import yaml

from tbot.utils.function import function_args2str, function_rets2str, check_obj_defined

config_path = "tbot/config/actions/OfficeAutomation/Word/WordFontColor/WordFontColor.yaml"
with open(config_path, "r", encoding="UTF-8") as f:
    config = yaml.safe_load(f)


def decorate_args(args, vars):
    # 在这里写下每个命令参数的特殊处理
    document = args.get("document", None)
    color = args.get("color", None)

    if document is None or not check_obj_defined(document, vars):
        raise TypeError(
            "输入的文档对象应当为一个已定义的对象变量，请确保先打开了一个文档，并且使用内存中已经定义的变量名")
    else:
        args["document"] = document
        args["color"] = color

    return args


def WordFontColor(args, vars):
    args = decorate_args(args, vars)
    args_str = function_args2str(config, args)
    return f"WordFontColor({args_str})"
