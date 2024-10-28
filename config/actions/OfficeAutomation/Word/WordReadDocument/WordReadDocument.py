import yaml

from tbot.services import BaseService
from tbot.utils.function import function_args2str, function_rets2str, check_obj_defined
from tbot.utils.function import convert2double_slash_path

class WordReadDocument(BaseService):
    def __init__(self, config_path):
        super().__init__(config_path)

    def forward(self, args, vars):
        rets = args.get("rets")
        if len(self.rets) != len(rets):
            raise Exception(f"函数 {self.name} 包含 {len(self.rets)} 个返回值，但是只配置了 {len(rets)} 个变量，请检查！")
        
        for ret_name, ret_var in zip(self.rets, rets):
            args.update({ret_name: ret_var})

        document = args.get("document", None)

        if document is None or not check_obj_defined(document, vars):
            raise TypeError("输入的文档对象应当为一个已打开的文档对象，请确保该文档已经被打开")
        else:
            args["document"] = document

        args_str = function_args2str(self.config, args)
        rets_str = function_rets2str(self.config, args)
        
        result = f"{rets_str} = WordReadDocument({args_str})"
        message = f"成功读取了文档 {document} 中的内容，输出到对象 {args['read_object']} 中。"
        return result, message

