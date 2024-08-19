import yaml

from utils.function import function_args2str, function_rets2str
from utils.function import convert2double_slash_path

config_path = "config/actions/FileOperation/common/CheckFileExists/CheckFileExists.yaml"
with open(config_path, "r", encoding="UTF-8") as f:
    config = yaml.safe_load(f)

def decorate_args(args):
    file_path = convert2double_slash_path(args.get("file_path"))
    args["file_path"] = f'\"{file_path}\"'
    return args

def CheckFileExists(args):
    args = decorate_args(args)
    args_str = function_args2str(config, args)
    rets_str = function_rets2str(config, args)
    return f"{rets_str}= CheckFileExists({args_str})"
