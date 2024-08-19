import yaml

from utils.function import function_args2str, function_rets2str
from utils.function import convert2double_slash_path

config_path = "config/actions/FileOperation/Pdf/PDFSetPwd/PDFSetPwd.yaml"
with open(config_path, "r", encoding="UTF-8") as f:
    config = yaml.safe_load(f)


def decorate_args(args):
    file_path = convert2double_slash_path(args["file_path"])
    args["file_path"] = f'\"{file_path}\"'
    save_path = convert2double_slash_path(args["save_path"])
    args["save_path"] = f'\"{save_path}\"'
    return args


def PDFSetPwd(args):
    args = decorate_args(args)
    args_str = function_args2str(config, args)
    return f"PDFSetPwd({args_str})"
