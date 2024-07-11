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
    
    #todo: add more actions
    #excel
    def excel_get_column_data(self, args):
        sheet_name = args.get("sheet_name")
        column_name = args.get("column_name")
        return f'ExcelGetColumnData(v_Excel, "{sheet_name}", "{column_name}", "0", "0", "false")'
    
    def excel_set_column(self, args):
        sheet_name = args.get("sheet_name")
        column_name = args.get("column_name")
        content = args.get("content")
        return f'ExcelSetColumn(v_Excel,“{sheet_name}”,“{column_name}”,"{content}",“是”,“0”,“0”,“false”)'
    
    def excel_insert_column(self, args):
        sheet_name = args.get("sheet_name")
        column_name = args.get("column_name")
        content = args.get("content")
        return f'ExcelInsertColumn(v_Excel,“{sheet_name}”,“{column_name}”,"{content}",“是”,“0”,“0”,“false”)'
    
    def excel_delete_column(self, args):
        sheet_name = args.get("sheet_name")
        column_name = args.get("column_name")
        return f'ExcelDeleteColumn(v_Excel,“{sheet_name}”,“{column_name}”,“是”,“0”,“0”,“false”)'

    def excel_get_row_number(self, args):
        sheet_name = args.get("sheet_name")
        return f'ExcelGetRowNumber(v_Excel,“{sheet_name}”,“0”,“0”,“false”)'

    def excel_get_column_number(self, args):
        sheet_name = args.get("sheet_name")
        return f'ExcelGetColumnNumber(v_Excel,“{sheet_name}”,“0”,“0”,“false”)'
    
    def excel_merge_cell(self, args):
        sheet_name = args.get("sheet_name")
        cell_name = args.get("cell_name")
        action_name = args.get("action_name")
        return f'ExcelMergeCell(v_Excel,“{sheet_name}”,“{cell_name}”,“{action_name}”,“是”,“0”,“0”,“false”)'
    
    def excel_column_width(self, args):
        sheet_name = args.get("sheet_name")
        column_name = args.get("column_name")
        width = args.get("width")
        return f'ExcelColumnWidth(v_Excel,“{sheet_name}”,“{column_name}”,“{width}”,“是”,“0”,“0”,“false”)'
    
    def excel_row_height(self, args):
        sheet_name = args.get("sheet_name")
        row_name = args.get("row_name")
        height = args.get("height")
        return f'ExcelRowHeight(v_Excel,“{sheet_name}”,“{row_name}”,“{height}”,“是”,“0”,“0”,“false”)'
    
    def excel_background_color(self, args):
        sheet_name = args.get("sheet_name")
        cell_name = args.get("cell_name")
        color = args.get("color")
        return f'ExcelBackgroundColor(v_Excel,“{sheet_name}”,“{cell_name}”,“{color}”,“是”,“0”,“0”,“false”)'
    
    def excel_font_color(self, args):
        sheet_name = args.get("sheet_name")
        cell_name = args.get("cell_name")
        color = args.get("color")
        return f'ExcelFontColor(v_Excel,“{sheet_name}”,“{cell_name}”,“{color}”,“是”,“0”,“0”,“false”)'
    
    def excel_get_font_color(self, args):
        sheet_name = args.get("sheet_name")
        cell_name = args.get("cell_name")
        return f'ExcelGetFontColor(v_Excel,“{sheet_name}”,“{cell_name}”,“0”,“0”,“false”)'
    
    def excel_add_worksheet(self, args):
        sheet_name = args.get("sheet_name") 
        aim_sheet_name = args.get("aim_sheet_name")
        return f'ExcelAddWorksheet(v_Excel,“{sheet_name}”,“{aim_sheet_name}”,“目标工作表之后”,“0”,“0”,“false”)'
    
    def excel_get_worksheet(self, args):
        return f'ExcelGetWorkSheet(v_Excel,“是”,“0”,“0”,“false”)'
    
    def excel_get_all_worksheet(self, args):
        return f'ExcelGetAllWorkSheet(v_Excel,“0”,“0”,“false”)'
    
    def excel_rename_worksheet(self, args):
        old_sheet_name = args.get("old_sheet_name")
        new_sheet_name = args.get("new_sheet_name")
        return f'ExcelRenameWorkSheet(v_Excel,“{old_sheet_name}”,“{new_sheet_name}”,“是”,“0”,“0”,“false”)'
    
    #file
    def read_text_file(self, args):
        file_path = args.get("file_path")
        return f'ReadTextFile(“{file_path}”,“Content”,“0”,“0”,“false”)'
    
    def write_text_file(self, args):
        file_path = args.get("file_path")
        content = args.get("content")
        return f'WriteTextFile(“{file_path}”,“{content}”,“Overwrite”,“0”,“0”,“false”)'
    
    def get_file_name(self, args):
        file_path = args.get("file_path")
        return f'GetFileName(“{file_path}”,“Yes”,“0”,“0”,“false”)'
    
    def get_file_extension(self, args):
        file_path = args.get("file_path")
        return f'GetFileExtension(“{file_path}”,“0”,“0”,“false”)'
    
    def get_parent_file(self, args):
        file_path = args.get("file_path")
        return f'GetParentFile(“{file_path}”,“0”,“0”,“false”)'
    
    def get_file_size(self, args):
        file_path = args.get("file_path")
        return f'GetFileSize(“{file_path}”,“0”,“0”,“false”)'
    
    def get_folder_size(self, args):
        folder_path = args.get("folder_path")
        return f'GetFolderSize(“{folder_path}”,“0”,“0”,“false”)'
    
    def move_file(self, args):
        action_name = args.get("action_name")#复制文件/移动文件
        source_file_path = args.get("source_file_path")
        target_folder_path = args.get("target_folder_path")
        return f'MoveFile(“{action_name}”,“{source_file_path}”,“{target_folder_path}”,“Yes”,“0”,“0”,“false”)'
    
    def move_folder(self, args):
        action_name = args.get("action_name")#复制文件夹/移动文件夹
        source_folder_path = args.get("source_folder_path")
        target_folder_path = args.get("target_folder_path")
        return f'MoveFolder(“{action_name}”,“{source_folder_path}”,“{target_folder_path}”,“No”,“0”,“0”,“false”)'
    
    def rename_file(self, args):
        file_path = args.get("file_path")
        new_file_name = args.get("new_file_name")
        return f'RenameFile(“{file_path}”,“{new_file_name}”,“0”,“0”,“false”)'
    
    def delete_file(self, args):
        file_path = args.get("file_path")
        return f'DeleteFile(“{file_path}”,“0”,“0”,“false”)'
    
    def delete_folder(self, args):
        folder_path = args.get("folder_path")
        return f'DeleteFolder(“{folder_path}”,“0”,“0”,“false”)'
    
    def create_folder(self, args):
        folder_path = args.get("folder_path")
        return f'CreateFolder(“{folder_path}”,“0”,“0”,“false”)'
    
    def check_file_exists(self, args):
        file_path = args.get("file_path")
        return f'CheckFileExists(“{file_path}”,“0”,“0”,“false”)'
    
    def check_folder_exists(self, args):
        folder_path = args.get("folder_path")
        return f'CheckFolderExists(“{folder_path}”,“0”,“0”,“false”)'
    

    def log(self, content):
        self.logger.log(content)

