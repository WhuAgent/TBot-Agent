import yaml

from utils.function import function_args2str, function_rets2str
from utils.function import convert2double_slash_path

config_path = "config/actions/FileOperation/Pdf/GetPDFMerge/GetPDFMerge.yaml"
with open(config_path, "r", encoding="UTF-8") as f:
    config = yaml.safe_load(f)


def decorate_args(args):
    file_path = convert2double_slash_path(args["file_path"])
    args["file_path"] = f'\"{file_path}\"'
    merge_path = convert2double_slash_path(args["merge_path"])
    args["merge_path"] = f'\"{merge_path}\"'
    return args


def GetPDFMerge(args):
    args = decorate_args(args)
    args_str = function_args2str(config, args)
    return f"GetPDFMerge({args_str})"
