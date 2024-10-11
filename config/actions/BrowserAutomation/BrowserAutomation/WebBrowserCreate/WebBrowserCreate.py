import os.path

import yaml

from utils.function import function_args2str, function_rets2str

config_path = os.path.join(os.path.dirname(__file__), "WebBrowserCreate.yaml")
with open(config_path, "r", encoding="UTF-8") as f:
    config = yaml.safe_load(f)


def decorate_args(args):
    if args.get("base_url"):
        args["base_url"] = f'\"{args["base_url"]}\"'
    return args


def WebBrowserCreate(args):
    args = decorate_args(args)
    args_str = function_args2str(config, args)
    rets_str = function_rets2str(config, args)
    return f"{rets_str} = WebBrowserCreate({args_str})"
