import yaml

from tbot.services import BaseService

from tbot.utils.function import function_args2str, function_rets2str, check_obj_defined
from tbot.utils.function import convert2double_slash_path


class WordAddDocument(BaseService):
    def __init__(self, config_path):
        super().__init__(config_path)

    def forward(self, args, vars):
        document = args.get("document", None)

        if document is None or not check_obj_defined(document, vars):
            raise TypeError("输入的文档对象应当为一个已打开的文档对象，请确保该文档已经被打开")

        args_str = function_args2str(self.config, args)

        result = f"WordAddDocument({args_str})"
        message = f"成功添加空白文档。"
        return result, message
