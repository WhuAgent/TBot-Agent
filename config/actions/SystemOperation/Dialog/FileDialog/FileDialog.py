# -*- coding:utf-8 -*-
"""
作者：86173
日期：2024年07月23日
"""
import yaml

from utils.function import function_args2str, function_rets2str
from utils.function import convert2double_slash_path

config_path = "config/actions/SystemOperation/Dialog/FileDialog/FileDialog.yaml"
with open(config_path, "r", encoding="UTF-8") as f:
    config = yaml.safe_load(f)


def decorate_args(args):
    # 暂时没想到需要处理的参数，可能需要将文件类型套一个引号
    file_type = args["file_type"]
    args["file_type"] = f'\"{file_type}\"'
    origin_path = convert2double_slash_path(args["origin_path"])
    args["origin_path"] = f'\"{origin_path}\"'
    return args


def FileDialog(args):
    args = decorate_args(args)
    args_str = function_args2str(config, args)
    rets_str = function_rets2str(config, args)
    return f"{rets_str} = FileDialog({args_str})"