import json

from tbot.utils import get_system_prompt, get_task_prompt
from utils.logger import Logger
from utils.llm import chat_llm


class TBotAgent:
    def __init__(self, task):
        self.logger = Logger(root="log/tbot/")

        self.model = "gpt-3.5-turbo"
        self.system_prompt = get_system_prompt()
        self.task_prompt = get_task_prompt(task)
        self.messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": self.task_prompt}
        ]
        for message in self.messages:
            self.log(f"{message['role']}:\n{message['content']}")

        self.action_func_map = {
            "WordCloseDocument": self.word_close_document,
            "WordOpenDocument": self.word_open_document,
            "WorldOverReadDocument": self.world_over_read_document
        }

    def plan(self):
        response = chat_llm(self.model, self.messages)
        self.log(f"{response.role}:\n{response.content}")
        self.messages.append({"role": response.role, "content": response.content})
        return json.loads(response.content)

    def step(self, action):
        action_name = action.get("action")
        action_args = action.get("args")

        # TODO: 一步一步交互时执行动作之后的 observation
        # config_path = f"model/tbot/action_observation_config/{action_name}.json"
        # with open(config_path, "r", encoding="UTF-8") as f:
        #     config = json.load(f)

        # try:
        #     result = self.action_func_map[action_name](action_args)
        # except Exception as e:
        #     observation = generate_observation(config[str(type(e).__name__)])
        # else:
        #     observation = generate_observation(config["Success"], **result)

        result = self.action_func_map[action_name](action_args)
        return result

    def word_close_document(self, args):
        return 'WordCloseDocument(v_Word,"是","0","0","false")'

    def word_open_document(self, args):
        file_path = args.get("file_path")
        return f'v_Word = WordOpenDocument("是","{file_path}","是","0","0","false")'

    def world_over_read_document(self, args):
        content = args.get("content")
        return f'WorldOverReadDocument(v_Word, "{content}","0","0","false")'

    def log(self, content):
        self.logger.log(content)

