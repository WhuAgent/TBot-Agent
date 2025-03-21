import yaml

from utils.function import function_args2str, function_rets2str
from utils.function import convert2double_slash_path

config_path = "config/actions/SystemOperation/System/RunPowershell/RunPowershell.yaml"
with open(config_path, "r", encoding="UTF-8") as f:
    config = yaml.safe_load(f)


def decorate_args(args):
    # 在这里写下每个命令参数的特殊处理
    ps_name = convert2double_slash_path(args["ps_name"])
    args["ps_name"] = f'\"{ps_name}\"'
    return args


def RunPowershell(args):
    args = decorate_args(args)
    args_str = function_args2str(config, args)
    rets_str = function_rets2str(config, args)
    return f"{rets_str} = RunPowershell({args_str})"
