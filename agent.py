import re
from copy import deepcopy

import pika
import json
import click
import traceback
import yaml

from agent_network.exceptions import RetryError, ReportError
from agent_network.base import BaseAgent
# from tbot.vectordb import TaskPlanVectorDB, CommandVectorDB
from tbot.util import task_abstraction, send_message, decorate_message, get_action_configs, convert2dict
from tbot.utils.function import dynamic_import
from tbot.type import Variable
from tbot.services import ServiceCallError

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
        if error_message := kwargs.get("graph_error_message"):
            prompt = f"在执行前一个任务的过程中，遇到了错误：\n\n{error_message}\n\n导致任务无法完成，请决定新的任务以解决这些错误"
        else:
            completed_tasks = json.dumps(kwargs["completed_tasks"], indent=4, ensure_ascii=False)
            prompt = f"当前用户的需求为：{kwargs['task']}\n\n已完成的子任务为：{completed_tasks}"
            prompt += f"\n\n请决定下一个需要完成的任务。"
            prompt += "\n可选择的 next_agent 包括：\n"
            for agent, description in kwargs.get("graph_next_executors").items():
                prompt += f"\n{agent}: {description}"
        self.add_message("user", prompt)
        response = chat_llm(self.model, self.messages)
        self.add_message(response.role, response.content)

        if response.content == "COMPLETE":
            results = {
                "next_task": "请输出生成的代码",
                "next_agent": "CodeExecutionGroup"
            }
        else:
            pattern = "###([\s\S]*?)###"
            data = re.findall(pattern, response.content)[0]
            data = yaml.safe_load(data)

            results = {
                "next_task": data.get("next_task"),
                "next_agent": data.get("execution_agent")
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

    def forward(self, message, **kwargs):
        results = {}
        for result in self.results:
            results[result["name"]] = deepcopy(kwargs.get(result["name"]))

        try:
            prompt = f"当前需要进行的操作为：{kwargs['next_task']}\n\n当前已完成的操作有：\n"
            prompt += f"{json.dumps(kwargs['completed_tasks'], indent=4, ensure_ascii=False)}"
            if errors := kwargs.get("graph_error_message"):
                error_message = json.dumps(errors, indent=4, ensure_ascii=False)
                prompt = f"{prompt}\n\n在之前的生成过程中，产生了如下错误: \n{error_message}\n\n "
                prompt += "导致服务没有调用成功，请重新生成对应的服务调用！"
            else:
                prompt += "\n\n请决定接下来要调用的服务"
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
                    if ret_var is None or ret_var.lower() == "none":
                        continue
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
            results["error_message"] = ""
            results["next_agent"] = "ManagerAgent"
        except Exception as e:
            import traceback
            traceback.print_exc()
            error_message = str(e)
            if e.__class__ == ServiceCallError:
                if "不要配置返回值" in error_message:
                    error_message = error_message.replace("不要配置返回值", "删除 rets 配置项")
                raise RetryError(error_message)
            else:
                prompt =  f"在调用服务的过程中遇到了错误：\n\n{error_message}\n\n 这意味着你支持的服务无法完成当前需要进行的操作。"
                prompt += f"请结合当前需要完成的操作，和错误细节，形成错误报告和解决方案，作为输出。"
                self.add_message("user", prompt)
                response = chat_llm(self.model, self.messages)
                self.add_message(response.role, response.content)
                raise ReportError(response.content, "ManagerAgent")

        return results


class WordOperationAgent(OperationAgent):
    def __init__(self, config, logger):
        super().__init__(config, logger)

class WordMouseKeyboardAgent(OperationAgent):
    def __init__(self, config, logger):
        super().__init__(config, logger)


class WordDocumentAgent(OperationAgent):
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


class WordFontSetAgent(OperationAgent):
    def __init__(self, config, logger):
        super().__init__(config, logger)


class CodeExecutionAgent(BaseAgent):
    def __init__(self, config, logger):
        super().__init__(config, logger)

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


class EndAgent(BaseAgent):
    def __init__(self, config, logger):
        super().__init__(config, logger)

    def initial_messages(self):
        pass

    def forward(self, message, **kwargs):
        return {"next_task": "COMPLETE"}
