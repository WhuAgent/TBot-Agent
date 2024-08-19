import yaml

from utils.function import function_args2str, function_rets2str
from utils.function import convert2double_slash_path

config_path = "config/actions/OfficeAutomation/Excel/ExcelMergeCell/ExcelMergeCell.yaml"
with open(config_path, "r", encoding="UTF-8") as f:
    config = yaml.safe_load(f)

def decorate_args(args):
    return args

def ExcelMergeCell(args):
    args = decorate_args(args)
    args_str = function_args2str(config, args)
    return f"ExcelMergeCell({args_str})"
