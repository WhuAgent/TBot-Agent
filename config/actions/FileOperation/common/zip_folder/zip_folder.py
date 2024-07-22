import yaml

from utils.function import function_args2str, function_rets2str
from utils.function import convert2double_slash_path

config_path = "config/actions/FileOperation/common/zip_folder/zip_folder.yaml"
with open(config_path, "r", encoding="UTF-8") as f:
    config = yaml.safe_load(f)


def decorate_args(args):
    # 在这里写下每个命令参数的特殊处理
    folder_path = convert2double_slash_path(args["folder_path"])
    args["folder_path"] = f'\"{folder_path}\"'
    target_path = convert2double_slash_path(args["target_path"])
    args["target_path"] = f'\"{target_path}\"'
    return args


def zip_folder(args):
    args = decorate_args(args)
    args_str = function_args2str(config, args)
    rets_str = function_rets2str(config, args)
    return f"{rets_str} = ZipFolder({args_str})"
