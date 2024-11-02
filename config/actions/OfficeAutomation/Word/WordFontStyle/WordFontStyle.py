
from tbot.services import BaseService
from tbot.utils.function import function_args2str, function_rets2str, check_obj_defined


class WordFontStyle(BaseService):
    def __init__(self, config_path):
        super().__init__(config_path)

    def forward(self, args, vars):
        document = args.get("document", None)
        bold = args.get("bold", None)
        italic = args.get("italic", None)
        underline = args.get("underline", None)

        if document is None or not check_obj_defined(document, vars):
            raise TypeError("输入的文档对象应当为一个已打开的文档对象，请确保该文档已经被打开")
        else:
            args["document"] = document
            args["bold"] = bold
            args["italic"] = italic
            args["underline"] = underline

        args_str = function_args2str(self.config, args)

        result = f"WordFontStyle({args_str})"
        message = f"成功更改了文档 {document} 中选择区域的文字的样式"
        return result, message
