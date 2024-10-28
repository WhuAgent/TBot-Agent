import yaml

from tbot.services import BaseService

from tbot.utils.function import function_args2str, function_rets2str
from tbot.utils.function import convert2double_slash_path


class WordOpenDocument(BaseService):
    def __init__(self, config_path):
        super().__init__(config_path)

    def forward(self, args, vars):
        
        args["file_path"] = convert2double_slash_path(args["file_path"])

        if args.get("word_object") is None:
            raise Exception("命令 WordOpenDocument 包含一个返回值 word_object ，表示打开的文档对象，请以 'word_object: var_name' 的方式为返回值 word_object 配置变量名！")

        args_str = function_args2str(self.config, args)
        rets_str = function_rets2str(self.config, args)
        
        result = f"{rets_str} = WordOpenDocument({args_str})"
        message = f"成功打开文档 {args['file_path']}，其文档对象被储存为 {args['word_object']}。"
        return result, message
