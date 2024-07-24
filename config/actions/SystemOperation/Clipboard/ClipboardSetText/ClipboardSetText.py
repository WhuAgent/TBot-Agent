# -*- coding:utf-8 -*-
"""
作者：86173
日期：2024年07月23日
"""
import yaml

from utils.function import function_args2str, function_rets2str
from utils.function import convert2double_slash_path

config_path = "config/actions/SystemOperation/Clipboard/ClipboardSetText/ClipboardSetText.yaml"
with open(config_path, "r", encoding="UTF-8") as f:
    config = yaml.safe_load(f)


def decorate_args(args):
    # 在这里写下每个命令参数的特殊处理
    content = args["content"]
    args["content"] = f'\"{content}\"'
    return args


def ClipboardSetText(args):
    args = decorate_args(args)
    args_str = function_args2str(config, args)
    return f"ClipboardSetText({args_str})"