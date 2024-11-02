import yaml

from tbot.services import BaseService
from tbot.utils.function import function_args2str, function_rets2str, check_obj_defined
from tbot.utils.function import convert2double_slash_path
from tbot.type import Variable


class WordSelectAll(BaseService):
    def __init__(self, config_path):
        super().__init__(config_path)

    def forward(self, args, vars):
        document = args.get("document", None)

        if document is None or not check_obj_defined(document, vars):
            raise TypeError("输入的文档对象应当为一个已打开的文档对象，请确保该文档已经被打开")
        args["document"] = document

        args_str = function_args2str(self.config, args)

        result = f"WordSelectAll({args_str})"
        message = f"成功全选文档 {document} 中的所有内容"
        return result, message