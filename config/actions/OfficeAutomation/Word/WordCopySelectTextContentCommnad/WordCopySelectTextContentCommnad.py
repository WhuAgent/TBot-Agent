import yaml

from tbot.services import BaseService
from tbot.utils.function import function_args2str, function_rets2str, check_obj_defined
from tbot.type import Variable

class WordCopySelectTextContentCommnad(BaseService):
    def __init__(self, config_path):
        super().__init__(config_path)

    def forward(self, args, vars):
        document = args.get("document", None)

        if document is None or not check_obj_defined(document, vars):
            raise TypeError("输入的文档对象应当为一个已打开的文档对象，请确保该文档已经被打开")
        else:
            args["document"] = document

        args_str = function_args2str(self.config, args)

        result = f"WordCopySelectTextContentCommnad({args_str})"
        message = f"成功复制了文档 {document} 中选择的内容到剪贴板"
        return result, message
