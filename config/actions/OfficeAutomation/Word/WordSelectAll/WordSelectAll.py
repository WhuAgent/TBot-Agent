import yaml

from utils.function import function_args2str, function_rets2str
from utils.function import convert2double_slash_path
from tbot.type import Variable

config_path = "tbot/config/actions/OfficeAutomation/Word/WordSelectAll/WordSelectAll.yaml"
with open(config_path, "r", encoding="UTF-8") as f:
    config = yaml.safe_load(f)


def decorate_args(args):
    # 在这里写下每个命令参数的特殊处理
    document = args.get("document", None)

    if document is None or type(document) is not Variable:
        raise TypeError("输入的文档对象应当为一个已定义的对象变量，请确保先打开了一个文档，并且使用内存中已经定义的变量名")
    else:
        args["document"] = document.name

    return args


def WordSelectAll(args):
    args = decorate_args(args)
    args_str = function_args2str(config, args)
    return f"WordSelectAll({args_str})"
