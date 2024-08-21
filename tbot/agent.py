import json
import re
import yaml

from tbot.vectordb import TaskVectorDB
from tbot.util import add_relevant_actions_prompt, get_action_configs, task_abstraction
from utils.logger import Logger
from utils.llm import chat_llm
from utils.function import dynamic_import


action_config = get_action_configs("config/actions")


class TBotAgent:
    def __init__(self, task):
        self.logger = Logger(root="log/tbot/")

        self.task = task
        self.abstracted_task = task_abstraction(self.task)
        self.taskdb = TaskVectorDB("manual")
        self.relevant_commands = self.taskdb.get_relevant_commands(self.abstracted_task)

        self.model = "gpt-3.5-turbo"
        self.prompt_path = "prompt/tbot.yaml"
        self.messages = self.get_prompt()
        for message in self.messages:
            self.log(f"{message['role']}:\n{message['content']}")

        self.plan = []

    def get_prompt(self):
        with open(self.prompt_path, "r", encoding="utf-8") as f:
            prompt = yaml.safe_load(f)
        system_prompt = prompt["system_prompt"]
        task_prompt = prompt["task_prompt"]
        task_prompt = task_prompt.replace("{task}", self.task)
        task_prompt = task_prompt.replace("{actions}", add_relevant_actions_prompt(self.relevant_commands, action_config))
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": task_prompt}
        ]


    def generate_plan(self):
        response = chat_llm(self.model, self.messages)
        self.log(f"{response.role}:\n{response.content}")
        self.messages.append({"role": response.role, "content": response.content})

        # 提取 json 字段
        pattern = r"```(?:json|yaml)?([\s\S]*?)```"
        plan = re.findall(pattern, response.content)
        plan = plan[0]
        self.plan = json.loads(plan)
        return self.plan

    def generate_code(self):
        variable_defines = []
        codes = []
        for step in self.plan:
            action = step["action"]
            args = step.get("args")
            if step.get("rets"):
                for variable in step.get("rets").values():
                    variable_defines.append(variable)
                args.update(step.get("rets"))
            action_module = action_config[action]["action_module"]
            _, action_func = dynamic_import(action_module, action)
            code = action_func(args)
            codes.append(code)

        # 代码拼接
        lines = []
        for variable in variable_defines:
            lines.append(f'Dim {variable} = \"\"')
        lines.append('\n')
        for code in codes:
            lines.append(code)

        return '\n'.join(lines)

    # def step(self, action):
    #     action_name = action.get("action")
    #     action_args = action.get("args")
    #
    #     # TODO: 一步一步交互时执行动作之后的 observation
    #     # config_path = f"model/tbot/action_observation_config/{action_name}.json"
    #     # with open(config_path, "r", encoding="UTF-8") as f:
    #     #     config = json.load(f)
    #
    #     # try:
    #     #     result = self.action_func_map[action_name](action_args)
    #     # except Exception as e:
    #     #     observation = generate_observation(config[str(type(e).__name__)])
    #     # else:
    #     #     observation = generate_observation(config["Success"], **result)
    #
    #     # result = self.action_func_map[action_name](action_args)
    #     # return result

    def log(self, content):
        self.logger.log(content)

