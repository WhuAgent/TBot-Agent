import yaml

from tbot.services import BaseService

from tbot.utils.function import function_args2str, function_rets2str, check_obj_defined

class WorldOverReadDocument(BaseService):
    def __init__(self, config_path):
        super().__init__(config_path)

    def forward(self, args, vars):
        document = args.get("document", None)

        if document is None or not check_obj_defined(document, vars):
            raise TypeError("输入的文档对象应当为一个已打开的文档对象，请确保该文档已经被打开")
        args["document"] = document

        args_str = function_args2str(self.config, args)

        result = f"WorldOverReadDocument({args_str})"
        message = f"成功重写文档 {document} 中的内容"
        return result, message
