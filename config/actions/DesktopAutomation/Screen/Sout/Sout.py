import os.path

import yaml

from utils.function import function_args2str, function_rets2str

config_path = os.path.abspath(__file__).replace(".py", ".yaml")
with open(config_path, "r", encoding="UTF-8") as f:
    config = yaml.safe_load(f)


def decorate_args(args):
    return args


def Sout(args):
    args = decorate_args(args)
    args_str = function_args2str(config, args)
    return f"PrintLogToForm({args_str})"
