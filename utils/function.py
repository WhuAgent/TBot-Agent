import importlib
import os


def check_obj_defined(obj, vars):
    for variable in vars:
        if obj == variable:
            return True
    return False

no_quote_tokens = ["true", "false"]

def function_args2str(config, args):
    buffer = []
    for key, value in config.get("args").items():
        val =  str(args.get(key, value))
        if val.lower() not in no_quote_tokens and not val.isdigit() and key not in config["variables"]:
            val = f'\"{val}\"'
        buffer.append(val)
    return ", ".join(buffer)


def function_rets2str(config, args):
    return ", ".join(f"{args.get(key)}" for key in config.get("rets"))


def dynamic_import(module_name, function_name):
    try:
        # 动态导入模块
        module = importlib.import_module(module_name)
        # 从模块中获取函数
        func = getattr(module, function_name)
        return module, func
    except ImportError:
        print(f"无法导入模块：{module_name}，请确保这是可调用的服务")
    except AttributeError:
        print(f"模块 {module_name} 中没有找到函数 {function_name}")


def convert2double_slash_path(path):
    # 将路径拆分为各部分
    parts = os.path.normpath(path).split(os.sep)
    # 重新组合路径
    return '\\\\'.join(parts)
