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
            "WordAddDocument": self.word_add_document,
            "WordCloseDocument": self.word_close_document,
            "WordCutSelectTextContentCommnad": self.word_cut_select_text_content_commnad,
            "WordExportToPDF": self.word_export_to_pdf,
            "WordGetFilePath": self.word_get_file_path,
            "WordMoveSetCursor": self.word_move_set_cursor,
            "WordOpenDocument": self.word_open_document,
            "WordReadDocument": self.word_read_document,
            "WordSave": self.word_save,
            "WordSaveAs": self.word_save_as,
            "WordSelectAll": self.word_select_all,
            "WordSelectLine": self.word_select_line,
            "WordSetCursorPosition": self.word_set_cursor_position,
            "WorkSelectTextContentPosition": self.work_select_text_content_position,
            "WorldOverReadDocument": self.world_over_read_document,

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


    def word_add_document(self, args):
        return 'WordAddDocument(v_Word,"0","0","false")'

    def word_close_document(self, args):
        return 'WordCloseDocument(v_Word,"是","0","0","false")'

    def word_save(self, args):
        return 'WordSave(v_Word, "0","0","false")'

    def word_save_as(self, args):
        file_path = args.get("file_path")
        return f'WordSaveAs(v_Word,"{file_path}","0","0","false")'

    def word_export_to_pdf(self, args):
        file_path = args.get("file_path")
        return f'WordExportToPDF(v_Word,"{file_path}","0","0","false")'

    def word_get_file_path(self, args):
        return 'v_Ret = WordGetFilePath(v_Word,"0","0","false")'

    def word_read_document(self, args):
        return 'v_Ret = WordReadDocument(v_Word,"0","0","false")'

    def word_set_cursor_position(self, args):
        move_num = args.get("move_num")
        move_type = args.get("move_type")
        return f'WordSetCursorPosition(v_Word,"{move_num}","{move_type}")'

    def work_select_text_content_position(self, args):
        content = args.get("content")
        curse_position = args.get("curse_position")
        return f'WorkSelectTextContentPosition(v_Word,"{content}","{curse_position}","0","0","false")'

    def word_move_set_cursor(self, args):
        move_num = args.get("move_num")
        move_type = args.get("move_type")
        move_direction = args.get("move_direction")
        is_press_shift = args.get("is_press_shift")
        return f'WordMoveSetCursor(v_Word,"{move_num}","{move_type}","{move_direction}","{is_press_shift}","0","0","false")'

    def word_select_line(self, args):
        start_line = args.get("start_line")
        end_line = args.get("end_line")
        return f'WordSelectLine(v_Word,"{start_line}","{end_line}","0","0","false")'

    def word_select_all(self, args):
        return 'WordSelectAll(v_Word,"0","0","false")'

    def word_cut_select_text_content_commnad(self, args):
        return 'WordCutSelectTextContentCommnad(v_Word,"0","0","false")'

    def word_open_document(self, args):
        file_path = args.get("file_path")
        return f'v_Word = WordOpenDocument("是","{file_path}","是","0","0","false")'

    def world_over_read_document(self, args):
        content = args.get("content")
        return f'WorldOverReadDocument(v_Word, "{content}","0","0","false")'

    def word_add_document(self, args):
        return 'WordAddDocument(v_Word, "0", "0", "false")'

    def word_save(self, args):
        return 'WordSave(v_Word, "0", "0", "false")'

    def log(self, content):
        self.logger.log(content)

