import yaml


class BaseService:
    def __init__(self, config_path) -> None:
        with open(config_path, "r", encoding="UTF-8") as f:
            self.config = yaml.safe_load(f)
        self.name = self.config["name"]
        self.args = self.config["args"]
        self.rets = self.config.get("rets", [])
        self.variables = self.config["variables"]
        
    def forward(self, args, vars):
        result = ""
        message = ""
        return result, message

    def __call__(self, args, vars):
        rets = args.get("rets")
        if len(self.rets) != len(rets):
            if len(self.rets) == 0:
                raise Exception(f"函数 {self.name} 没有返回值，返回值的配置请留空！")
            else:
                raise Exception(f"函数 {self.name} 包含 {len(self.rets)} 个返回值，但是配置了 {len(rets)} 个变量，请检查并修正错误！")
        
        for ret_name, ret_var in zip(self.rets, rets):
            args.update({ret_name: ret_var})

        try:
            result, message = self.forward(args, vars)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return False, "", str(e)
        else:
            return True, result, message