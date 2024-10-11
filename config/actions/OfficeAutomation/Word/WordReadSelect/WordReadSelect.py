import yaml

from utils.function import function_args2str, function_rets2str

config_path = "config/actions/OfficeAutomation/Word/WordReadSelect/WordReadSelect.yaml"
with open(config_path, "r", encoding="UTF-8") as f:
    config = yaml.safe_load(f)


def decorate_args(args):
    # 在这里写下每个命令参数的特殊处理
    return args


def WordReadSelect(args):
    args = decorate_args(args)
    args_str = function_args2str(config, args)
    rets_str = function_rets2str(config, args)
    return f"{rets_str} = WordReadSelect({args_str})"
