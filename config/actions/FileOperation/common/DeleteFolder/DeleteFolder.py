import yaml

from utils.function import function_args2str, function_rets2str
from utils.function import convert2double_slash_path

config_path = "config/actions/FileOperation/common/DeleteFolder/DeleteFolder.yaml"
with open(config_path, "r", encoding="UTF-8") as f:
    config = yaml.safe_load(f)

def decorate_args(args):
    folder_path = convert2double_slash_path(args.get("folder_path"))
    args["folder_path"] = f'\"{folder_path}\"'
    return args

def DeleteFolder(args):
    args = decorate_args(args)
    args_str = function_args2str(config, args)
    return f"DeleteFolder({args_str})"
