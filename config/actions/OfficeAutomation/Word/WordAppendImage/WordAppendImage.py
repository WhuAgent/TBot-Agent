import yaml
import os
from tbot.services import BaseService
from tbot.utils.function import function_args2str, function_rets2str, check_obj_defined
from tbot.utils.function import convert2double_slash_path


class WordAppendImage(BaseService):
    def __init__(self, config_path):
        super().__init__(config_path)

    def forward(self, args, vars):
        file_path = convert2double_slash_path(args["file_path"])
        args["file_path"] = file_path
        document=args.get("document", None)
        if document is None or not check_obj_defined(document, vars):
            raise TypeError("输入的文档对象应当为一个已定义的对象变量，请确保先打开了一个文档，并且使用内存中已经定义的变量名")
        else:
            args["document"] = document

        args_str = function_args2str(self.config, args)

        result = f"WordAppendImage({args_str})"
        message = f"成功向文档 {document} 中插入图片，图片位置为 {file_path} "
        return result, message