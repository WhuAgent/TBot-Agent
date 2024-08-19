import os.path

import yaml

from utils.function import function_args2str, function_rets2str, convert2double_slash_path

config_path = os.path.abspath(__file__).replace(".py", ".yaml")
with open(config_path, "r", encoding="UTF-8") as f:
    config = yaml.safe_load(f)


def decorate_args(args):
    args["path"] = convert2double_slash_path(args["path"])
    return args


def ScreenShot(args):
    args = decorate_args(args)
    args_str = function_args2str(config, args)
    return f"ScreenShot({args_str})"
