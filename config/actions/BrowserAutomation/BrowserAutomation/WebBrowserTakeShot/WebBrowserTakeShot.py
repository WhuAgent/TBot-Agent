
import os.path

import yaml

from utils.function import function_args2str, function_rets2str, convert2double_slash_path

config_path = os.path.join(os.path.dirname(__file__), "WebBrowserTakeShot.yaml")
with open(config_path, "r", encoding="UTF-8") as f:
    config = yaml.safe_load(f)


def decorate_args(args):
    # 在这里写下每个命令参数的特殊处理
    file_path = convert2double_slash_path(args["file_path"])
    args["file_path"] = f'\"{file_path}\"'
    x = args.get("x")
    y = args.get("y")
    width = args.get("width")
    height = args.get("height")
    args["scope"] = f'\"[{x},{y},{width},{height}]\"'
    args.pop("x")
    args.pop("y")
    args.pop("width")
    args.pop("height")
    return args


def WebBrowserTakeShot(args):
    args = decorate_args(args)
    args_str = function_args2str(config, args)
    # rets_str = function_rets2str(config, args)
    return f"WebBrowserTakeShot({args_str})"
