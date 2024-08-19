import os.path

import yaml

from utils.function import function_args2str, function_rets2str

config_path = os.path.abspath(__file__).replace(".py", ".yaml")
with open(config_path, "r", encoding="UTF-8") as f:
    config = yaml.safe_load(f)


def decorate_args(args):
    return args


def GetElementHandle(args):
    args = decorate_args(args)
    # args_str = function_args2str(config, args)
    element_name = args.get("element_name")
    rets_str = function_rets2str(config, args)
    # 股票网站 列表内容
    # handle_obj =     # handle_obj = '"{\\"win\\":[{\\"Project\\":\\"chrome\\",\\"Title\\":\\"*Google Chrome*\\",\\"ClassName\\":\\"Chrome_WidgetWin_1\\"},{\\"LocalizedControlType\\":\\"分组\\"}],\\"web\\":[{\\"class\\":\\"clearfix\\",\\"parentid\\":\\"root\\",\\"tag\\":\\"div\\"}]}"'
    # github setting 复选框
    # handle_obj =
    # excel
    # handle_obj =
    # baidu
    handle_obj_dict = {
        "Google Chrome股票列表": '"{\\"win\\":[{\\"Project\\":\\"chrome\\",\\"Title\\":\\"*Google Chrome*\\",\\"ClassName\\":\\"Chrome_WidgetWin_1\\"},{\\"LocalizedControlType\\":\\"文字\\",\\"Name\\":\\"430489\\"}],\\"web\\":[{\\"parentid\\":\\"table\\",\\"tag\\":\\"a\\",\\"text\\":\\"430489\\"}]}"',
        "下一页按钮": '"{\\"win\\":[{\\"Project\\":\\"chrome\\",\\"Title\\":\\"*Google Chrome*\\",\\"ClassName\\":\\"Chrome_WidgetWin_1\\"},{\\"LocalizedControlType\\":\\"文字\\",\\"Name\\":\\">\\"}],\\"web\\":[{\\"parentid\\":\\"root\\",\\"tag\\":\\"a\\",\\"text\\":\\">\\"}]}"',
        "Github setting复选框": '"{\\"win\\":[{\\"Project\\":\\"chrome\\",\\"Title\\":\\"*Google Chrome*\\",\\"ClassName\\":\\"Chrome_WidgetWin_1\\"},{\\"LocalizedControlType\\":\\"复选框\\",\\"Name\\":\\"Issues\\"}],\\"web\\":[{\\"xpath\\":\\"/html/body/div[1]/div[5]/div/main/turbo-frame/div/div/div[2]/div/div/div/div[4]/form[1]/div[2]/div/input[2]\\"}]}"',
        "excel列表": '"{\\"win\\":[{\\"Project\\":\\"excel\\",\\"Title\\":\\"设置单元格格式\\",\\"ClassName\\":\\"bosa_sdm_XL9\\"},{\\"Name\\":\\"分类(C):\\",\\"XPath\\":\\"/List[1]\\"}]}"',
        "百度搜索框": '"{\\"win\\":[{\\"Project\\":\\"chrome\\",\\"Title\\":\\"*Google Chrome*\\",\\"ClassName\\":\\"Chrome_WidgetWin_1\\"},{\\"LocalizedControlType\\":\\"可编辑文本\\"}],\\"web\\":[{\\"id\\":\\"kw\\",\\"tag\\":\\"input\\"}]}"'
    }

    if element_name == "Google Chrome股票列表下一页按钮":
        element_name = "下一页按钮"

    handle_obj = handle_obj_dict[element_name]

    return f"{rets_str} = {handle_obj}"
