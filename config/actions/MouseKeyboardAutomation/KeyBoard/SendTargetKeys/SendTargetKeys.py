import yaml

from utils.function import function_args2str, function_rets2str

config_path = "config/actions/MouseKeyboardAutomation/KeyBoard/SendTargetKeys/SendTargetKeys.yaml"
with open(config_path, "r", encoding="UTF-8") as f:
    config = yaml.safe_load(f)

target_path = '"{\\"win\\":[{\\"Project\\":\\"searchapp\\",\\"Title\\":\\"搜索\\",\\"ClassName\\":\\"Windows.UI.Core.CoreWindow\\"},{\\"Name\\":\\"name\\",\\"XPath\\": \\"/Edit\\"}]}"'
def target_nl_to_tbot(nl):
    dic = {
        "任务栏": "Shell_TrayWnd",
        "桌面": "SysListView32",
    }
    return dic[nl]

def get_target_path(args):
    area = args.get("area")
    name = args.get("name")
    return target_path.replace("class_type", target_nl_to_tbot(area)).replace("name", name)


def decorate_args(args):
    # 在这里写下每个命令参数的特殊处理
    args["area"] = get_target_path(args)
    args["name"] = f'\"{args["name"]}\"'
    return args


def SendTargetKeys(args):
    args = decorate_args(args)
    args_str = function_args2str(config, args)
    return f"SendTargetKeys({args_str})"
