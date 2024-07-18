import yaml

from utils.function import function_args2str, function_rets2str
from utils.function import convert2double_slash_path

config_path = "config/actions/FileOperation/common/MoveFolder/MoveFolder.yaml"
with open(config_path, "r", encoding="UTF-8") as f:
    config = yaml.safe_load(f)

def decorate_args(args):
    source_folder_path = convert2double_slash_path(args.get("source_folder_path"))
    args["source_folder_path"] = f'\"{source_folder_path}\"'
    target_folder_path = convert2double_slash_path(args.get("target_folder_path"))
    args["target_folder_path"] = f'\"{target_folder_path}\"'
    return args

def MoveFolder(args):
    args = decorate_args(args)
    args_str = function_args2str(config, args)
    return f"MoveFolder({args_str})"
