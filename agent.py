import re
from copy import deepcopy

import pika
import json
import click
import traceback
import yaml

from agent_network.base import BaseAgent
# from tbot.vectordb import TaskPlanVectorDB, CommandVectorDB
from tbot.util import task_abstraction, send_message, decorate_message, get_action_configs, convert2dict
from tbot.utils.function import dynamic_import
from tbot.type import Variable

from tbot.utils.llm import chat_llm

action_config = get_action_configs("tbot/config/actions")


class ManagerAgent(BaseAgent):
    def __init__(self, config, logger):
        super().__init__(config, logger)

    def initial_messages(self):
        for prompt in self.config["prompts"]:
            if prompt["type"] == "inline" and prompt["role"] == "system":
                self.add_message(prompt["role"], prompt["content"])

    def forward(self, message, **kwargs):
        if error_message := kwargs["error"]:
            prompt = f"在执行前一个任务的过程中，遇到了错误：\n\n{error_message}\n\n导致任务无法完成，请决定新的任务以解决这些错误"
        else:
            completed_tasks = json.dumps(kwargs["completed_tasks"], indent=4, ensure_ascii=False)
            prompt = f"当前用户的需求为：{kwargs['task']}\n\n已完成的子任务为：{completed_tasks}\n\n请决定下一个需要完成的任务。如打开文档 A。"
        self.add_message("user", prompt)
        response = chat_llm(self.model, self.messages)
        self.add_message(response.role, response.content)

        pattern = "###([\s\S]*?)###"
        data = re.findall(pattern, response.content)[0]
        data = yaml.safe_load(data)

        results = {
            "next_task": data["next_task"],
            "next_agent": data["execution_agent"]
        }
        return results


class OperationAgent(BaseAgent):
    def __init__(self, config, logger):
        super().__init__(config, logger)

    @staticmethod
    def add_service(prompt, services):
        service_prompt = ""
        for service in services:
            prompt_path = action_config[service]["prompt_path"]
            with open(prompt_path, "r", encoding="UTF-8") as f:
                service_prompt = f"{service_prompt}{f.read()}\n\n"
        prompt = prompt.replace("{services}", service_prompt)
        return prompt

    def initial_messages(self):
        for prompt in self.config["prompts"]:
            if prompt["type"] == "inline" and prompt["role"] == "system":
                content = deepcopy(prompt["content"])
                content = OperationAgent.add_service(content, self.config["services"])
                self.add_message(prompt["role"], content)

    @staticmethod
    def check_var_name(var_name, variables):
        for variable in variables:
            if variable["name"] == var_name:
                return False
        return True

    def forward(self, message, errors=[], **kwargs):
        results = {}
        for result in self.results:
            results[result["name"]] = deepcopy(kwargs.get(result["name"]))

        try:
            prompt = f"当前需要进行的操作为：{kwargs['next_task']}\n\n当前已完成的操作有：\n"
            prompt += f"{json.dumps(kwargs['completed_tasks'], indent=4, ensure_ascii=False)}"
            prompt += "\n\n请决定接下来要调用的服务"
            # for variable in kwargs["variables"]:
            #     prompt = f"{prompt}\n{variable['think']}"
            if len(errors) > 0:
                error_message = json.dumps(errors, indent=4, ensure_ascii=False)
                prompt = f"{prompt}\n\n在之前的生成过程中，产生了如下错误: \n {error_message}\n\n 请注意修复！"
            self.add_message("user", prompt)
            response = chat_llm(self.model, self.messages)
            self.add_message(response.role, response.content)

            pattern = "###([\s\S]*?)###"
            data = re.findall(pattern, response.content)[0]
            services = yaml.safe_load(data)

            for service in services:
                service_name = service["name"]
                args = service.get("args")
                rets = service.get("rets", [])
                for ret_var in rets:
                    if ret_var in results["variables"]:
                        raise Exception("变量名和已有的变量重复")
                    results["variables"].append(ret_var)
                args.update({"rets": rets})
                service_module = action_config[service_name]["action_module"]
                _, service = dynamic_import(service_module, service_name)
                service = service(action_config[service_name]["config_path"])
                success, result, message = service(args, results["variables"])
                if success:
                    results["code"].append(result)
                    results["completed_tasks"].append(message)
                else:
                    raise Exception(message)
            results["error"] = ""
            results["next_agent"] = "ManagerAgent"
        except Exception as e:
            import traceback
            traceback.print_exc()
            if e.__class__ == KeyError:
                error_message = "请确保要调用的服务 name 被正确设置"
            else:
                error_message = str(e)
            errors.append(error_message)
            if len(errors) <= 5:
                return self.forward("", errors, **kwargs)
            else:
                results["error"] = json.dumps(errors, indent=4, ensure_ascii=False)
                results["next_agent"] = "ManagerAgent"

        return results

class WordOperationAgent(OperationAgent):
    def __init__(self, config, logger):
        super().__init__(config, logger)


class ExcelOperationAgent(OperationAgent):
    def __init__(self, config, logger):
        super().__init__(config, logger)


class WordFileManageAgent(OperationAgent):
    def __init__(self, config, logger):
        super().__init__(config, logger)


class WordTextContentAgent(OperationAgent):
    def __init__(self, config, logger):
        super().__init__(config, logger)


class CodeExecutionAgent(BaseAgent):
    def __init__(self, config, logger):
        super().__init__(config, logger)
        self.initial_messages()

    def initial_messages(self):
        pass

    def forward(self, message, **kwargs):
        code = kwargs.get("code")
        variables = kwargs.get("variables")

        lines = []
        for var_name in variables:
            lines.append(f'Dim {var_name} = \"\"')
        lines.append("\n")

        lines.extend(code)
        code_content = "\n".join(lines)
        # print(code_content)
        results = {
            "next_task": "COMPLETE"
        }
        self.log("assistant", code_content)
        return results

