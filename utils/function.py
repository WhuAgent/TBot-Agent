import importlib
import os


def function_args2str(config, args):
    return ", ".join(f'\"{args.get(key, value)}\"' for key, value in config.get("args").items())


def function_rets2str(config, args):
    return ", ".join(f"{args.get(key, value)}" for key, value in config.get("rets").items())


def dynamic_import(module_name, function_name):
    try:
        # 动态导入模块
        module = importlib.import_module(module_name)
        # 从模块中获取函数
        func = getattr(module, function_name)
        return module, func
    except ImportError:
        print(f"无法导入模块：{module_name}")
    except AttributeError:
        print(f"模块 {module_name} 中没有找到函数 {function_name}")


def convert2double_slash_path(path):
    # 将路径拆分为各部分
    parts = os.path.normpath(path).split(os.sep)
    # 重新组合路径
    return '\\\\'.join(parts)
