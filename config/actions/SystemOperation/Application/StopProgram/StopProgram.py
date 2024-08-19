# -*- coding:utf-8 -*-
"""
作者：86173
日期：2024年07月23日
"""
import yaml

from utils.function import function_args2str, function_rets2str
from utils.function import convert2double_slash_path

config_path = "config/actions/SystemOperation/Application/StopProgram/StopProgram.yaml"
with open(config_path, "r", encoding="UTF-8") as f:
    config = yaml.safe_load(f)


def decorate_args(args):
    # 字符串名称应该不需要处理
    process_name = args["process_name"]
    args["process_name"] = f'\"{process_name}\"'
    return args


def StopProgram(args):
    args = decorate_args(args)
    args_str = function_args2str(config, args)
    return f"StopProgram({args_str})"