import yaml

from tbot.services import BaseService
from tbot.utils.function import function_args2str, function_rets2str, check_obj_defined, convert2double_slash_path


class WordExportToPDF(BaseService):
    def __init__(self, config_path):
        super().__init__(config_path)

    def forward(self, args, vars):
        document = args.get("document", None)
        file_path = args.get("file_path", None)

        if file_path is None:
            raise TypeError("需要导出的PDF的文件路径不存在，请输入文件路径")
        file_path = convert2double_slash_path(file_path)
        if document is None or not check_obj_defined(document, vars):
            raise TypeError("需要被导出为PDF的文档对象应当为一个已打开的文档对象，请确保该文档已经被打开")

        args_str = function_args2str(self.config, args)

        result = f"WordExportToPDF({args_str})"
        message = f"成功导出当前文档为PDF {document} 文件路径为 {file_path}"
        return result, message
