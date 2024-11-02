import yaml

from tbot.services import BaseService
from tbot.utils.function import function_args2str, function_rets2str, check_obj_defined


class WordGetFilePath(BaseService):
    def __init__(self, config_path):
        super().__init__(config_path)

    def forward(self, args, vars):
        document = args.get("document", None)

        if document is None or not check_obj_defined(document, vars):
            raise TypeError("需要获取文件路径的文档对象应当为一个已打开的文档对象，请确保该文档已经被打开")

        args_str = function_args2str(self.config, args)

        result = f"WordGetFilePath({args_str})"
        message = f"成功获取文件路径的文档 {document}"
        return result, message
