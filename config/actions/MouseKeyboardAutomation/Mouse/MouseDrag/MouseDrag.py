import yaml

from utils.function import function_args2str, function_rets2str

config_path = "config/actions/MouseKeyboardAutomation/Mouse/MouseDrag/MouseDrag.yaml"
with open(config_path, "r", encoding="UTF-8") as f:
    config = yaml.safe_load(f)


def decorate_args(args):
    # 在这里写下每个命令参数的特殊处理
    args["start_point"] = f'\"{args["start_point"]}\"'
    args["end_point"] = f'\"{args["end_point"]}\"'
    return args


def MouseDrag(args):
    args = decorate_args(args)
    args_str = function_args2str(config, args)
    return f"MouseDrag({args_str})"
