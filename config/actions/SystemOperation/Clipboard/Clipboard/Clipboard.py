# -*- coding:utf-8 -*-
"""
作者：86173
日期：2024年07月23日
"""
import yaml

from utils.function import function_args2str, function_rets2str
from utils.function import convert2double_slash_path

config_path = "config/actions/SystemOperation/Clipboard/Clipboard/Clipboard.yaml"
with open(config_path, "r", encoding="UTF-8") as f:
    config = yaml.safe_load(f)




def Clipboard(args):
    rets_str = function_rets2str(config, args)
    return f"{rets_str} = Clipboard(\"0\",\"0\",\"false\")"