import yaml

from utils.function import function_args2str, function_rets2str
from utils.function import convert2double_slash_path

config_path = "config/actions/FileOperation/Pdf/GetPDFAppointPicture/GetPDFAppointPicture.yaml"
with open(config_path, "r", encoding="UTF-8") as f:
    config = yaml.safe_load(f)


def decorate_args(args):
    file_path = convert2double_slash_path(args["file_path"])
    args["file_path"] = f'\"{file_path}\"'
    picture_path = convert2double_slash_path(args["picture_path"])
    args["picture_path"] = f'\"{picture_path}\"'
    if "password" in args:
        args["password"] = f'\"{args["password"]}\"'
    return args


def GetPDFAppointPicture(args):
    args = decorate_args(args)
    args_str = function_args2str(config, args)
    return f"GetPDFAppointPicture({args_str})"
