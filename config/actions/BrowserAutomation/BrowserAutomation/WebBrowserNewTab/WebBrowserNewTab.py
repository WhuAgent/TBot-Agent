
import os.path

import yaml

from utils.function import function_args2str, function_rets2str

config_path = os.path.join(os.path.dirname(__file__), "WebBrowserNewTab.yaml")
with open(config_path, "r", encoding="UTF-8") as f:
    config = yaml.safe_load(f)


def decorate_args(args):
    # 在这里写下每个命令参数的特殊处理
    if args.get("url"):
        args["url"] = f'\"{args["url"]}\"'
    return args


def WebBrowserNewTab(args):
    args = decorate_args(args)
    args_str = function_args2str(config, args)
    # rets_str = function_rets2str(config, args)
    return f"WebBrowserNewTab({args_str})"
