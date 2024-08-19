import yaml

from utils.function import function_args2str, function_rets2str
from utils.function import convert2double_slash_path

config_path = "config/actions/FileOperation/common/MoveFile/MoveFile.yaml"
with open(config_path, "r", encoding="UTF-8") as f:
    config = yaml.safe_load(f)

def decorate_args(args):
    source_file_path = convert2double_slash_path(args.get("source_file_path"))
    args["source_file_path"] = f'\"{source_file_path}\"'
    target_folder_path = convert2double_slash_path(args.get("target_folder_path"))
    args["target_folder_path"] = f'\"{target_folder_path}\"'
    return args

def MoveFile(args):
    args = decorate_args(args)
    args_str = function_args2str(config, args)
    return f"MoveFile({args_str})"
