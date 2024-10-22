import yaml

from tbot.utils.function import function_args2str, function_rets2str
from tbot.utils.function import convert2double_slash_path

config_path = "tbot/config/actions/OfficeAutomation/Word/WordOpenDocument/WordOpenDocument.yaml"
with open(config_path, "r", encoding="UTF-8") as f:
    config = yaml.safe_load(f)


def decorate_args(args):
    # 在这里写下每个命令参数的特殊处理
    file_path = convert2double_slash_path(args["file_path"])
    args["file_path"] = file_path

    if args.get("word_object") is None:
        raise Exception("命令 WordOpenDocument 包含一个返回值，表示打开的文档对象，请配置返回值变量名！")

    return args


def WordOpenDocument(args, vars):
    args = decorate_args(args)
    args_str = function_args2str(config, args)
    rets_str = function_rets2str(config, args)
    return f"{rets_str} = WordOpenDocument({args_str})"
