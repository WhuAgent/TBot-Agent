import re
import pika
import json
import click
import traceback
import yaml

from agent_network.base import BaseAgent
from tbot.vectordb import TaskPlanVectorDB, CommandVectorDB
from tbot.util import task_abstraction, send_message, decorate_message, get_action_configs, convert2dict
from utils.function import dynamic_import
from tbot.type import Variable

action_config = get_action_configs("tbot/config/actions")


class PlanAgent(BaseAgent):
    def __init__(self, config_path, logger, context):
        self.task_plan_db = TaskPlanVectorDB("tbot/manual/plan")

        super().__init__(config_path, logger, context)


    def on_message(self, channel, method, properties, body):
        message_from = properties.headers.get("message_from")
        body = body.decode("UTF-8")
        if body == "complete":
            self.channel.stop_consuming()
            return
        # self.log(message_from, body)
        self.forward(message_from, body)

    def before_agent(self, content):
        # click.echo(click.style("OK", fg="green"))
        abstracted_task = task_abstraction(self.task)
        relevant_plans = self.task_plan_db.get_relevant_plans(abstracted_task)

        references = ""
        for index, item in enumerate(relevant_plans):
            references += f"任务 {index + 1}:\n"
            references += f"{item['task']}\n"
            references += f"计划 {index + 1}: \n"
            references += f"{json.dumps(item['plan'], indent=4, ensure_ascii=False)}\n\n"

        details = {
            "task": self.retrieve("task"),
            "plans": references
        }

        content = decorate_message(content, **details)
        return content


    def after_agent(self, success, result, message_to, context):
        for key, value in context.items():
            self.register(key, value)

        message = self.get_prompt("after_plan")

        header = {"message_from": self.class_name}
        send_message(message_to, header, message)

    def execute(self, response_content):
        pattern = "###([\s\S]*?)###"
        data = re.findall(pattern, response_content)[-1]
        data = yaml.safe_load(data)
        result = data["plan"]
        message_to = data["message_to"]
        context = {"plan": data["plan"]}
        return True, result, message_to, context

class ExecutionAgent(BaseAgent):
    def __init__(self, config_path, logger, context):
        super().__init__(config_path, logger, context)

    def on_message(self, channel, method, properties, body):
        message_from = properties.headers.get("message_from")
        body = body.decode("UTF-8")
        if body == "complete":
            self.channel.stop_consuming()
            return
        # click.echo(click.style(json.dumps(self.context, indent=4, ensure_ascii=False), fg="green"))
        # print(f"ExecutionAgent Received: {body}")
        self.forward(message_from, body)

    def before_agent(self, content):
        details = {
            "task": self.retrieve("task"),
            "plan": self.retrieve("plan"),
            "cur_action": self.retrieve("cur_action"),
            "history_actions": self.retrieve("history_actions")
        }

        content = decorate_message(content, **details)
        return content

    def execute(self, response_content):
        pattern = "###([\s\S]*?)###"
        data = re.findall(pattern, response_content)[-1]
        data = yaml.safe_load(data)

        result = data["action"]
        message_to = data["message_to"]
        new_context = {
            "cur_action": data["action"]
        }

        return True, result, message_to, new_context

    def after_agent(self, success, result, message_to, context):
        if result == "complete":
            self.register("complete", True)
            return
        for key, value in context.items():
            self.register(key, value)

        click.echo(click.style(json.dumps(self.context, indent=4, ensure_ascii=False, default=convert2dict), fg="green"))

        message = self.get_prompt("after_one_step")

        header = {"message_from": self.class_name}
        send_message(message_to, header, message)


class ServiceAgent(BaseAgent):
    def __init__(self, config_path, logger, context):
        self.command_db = CommandVectorDB("tbot/manual/action")

        super().__init__(config_path, logger, context)


    def on_message(self, channel, method, properties, body):
        message_from = properties.headers.get("message_from")
        body = body.decode("UTF-8")
        if body == "complete":
            self.channel.stop_consuming()
            return
        # print(f"ServiceAgent Received: {body}")
        self.forward(message_from, body)

    def before_agent(self, content):
        cur_action = self.retrieve("cur_action")
        error = self.retrieve("error")
        task = self.retrieve("task")

        relevant_commands = self.command_db.get_relevant_commands(cur_action)
        manual = ""
        for command in relevant_commands:
            prompt_path = action_config[command]["prompt_path"]
            with open(prompt_path, "r", encoding="UTF-8") as f:
                manual = f"{manual}{f.read()}\n\n"

        varibles = self.retrieve("variable_memory")
        if varibles is None:
            varibles = "None"

        details = {
            "task": task,
            "error": error,
            "cur_action": cur_action,
            "manual": manual,
            "variables": varibles,
        }

        content = decorate_message(content, **details)
        return content

    def execute(self, response_content):
        pattern = "###([\s\S]*?)###"
        data = re.findall(pattern, response_content)[-1]
        data = yaml.safe_load(data)

        new_context = dict()

        command_name = data["command"]
        if command_name == "ExecutionReflexion":
            new_context = {"message": data["think"]}
            return False, "ExecutionReflexion", data["message_to"], new_context
        else:
            args = dict()
            if data.get("args"):
                for arg_name, arg_value in data["args"].items():
                    val = self.find_variables(arg_value)
                    args[arg_name] = val if val else arg_value
                    if val:
                        print(type(val), val)
                        print(args[arg_name])
            if data.get("rets"):
                for ret_data in data["rets"]:
                    think = f"打开的 {data['args']['file_path']} 文档对象"
                    new_variable = Variable(ret_data["var_name"], think)
                    if self.context["variable_memory"] and ret_data["var_name"] in self.context["variable_memory"]:
                        new_context = {"error": "返回值使用的变量名与已有的变量名重复"}
                        return False, "", "ServiceAgent", new_context
                    if "variable_memory" not in new_context.keys():
                        new_context["variable_memory"] = []
                    new_context["variable_memory"].append(new_variable)
                    args.update({ret_data["ret_name"]: new_variable})
            action_module = action_config[command_name]["action_module"]
            _, action_func = dynamic_import(action_module, command_name)
            try:
                code = action_func(args)
                new_context["code"] = code
            except Exception as e:
                traceback.print_exc()
                new_context = {"error": str(e)}
                return False, "", "ServiceAgent", new_context

            return True, code, "ExecutionAgent", new_context

    def after_agent(self, success, result, message_to, context):
        click.echo(success)
        click.echo(result)
        click.echo(message_to)
        click.echo(json.dumps(context, indent=4, ensure_ascii=False, default=convert2dict))
        # click.echo(click.style(json.dumps(self.context, indent=4, ensure_ascii=False, default=convert2dict), fg="green"))
        # input()

        if result == "ExecutionReflexion":
            message = context["message"]
            send_message(message_to, {"message_from": self.class_name}, message)
            return

        if context:
            for key, value in context.items():
                if key == "code":
                    if self.context[key] is None:
                        self.context[key] = []
                    self.context[key].append(value)
                elif key == "variable_memory":
                    if self.context[key] is None:
                        self.context[key] = []
                    self.context[key].extend(value)
                else:
                    self.register(key, value)

        if success:
            if self.context["history_actions"]:
                self.context["history_actions"].append(self.context["cur_action"])
            else:
                self.context["history_actions"] = [self.context["cur_action"]]
            message = self.get_prompt("success_after_agent")
            send_message(message_to, {"message_from": self.class_name}, message)
        else:
            if message_to == "ServiceAgent":
                message = self.get_prompt("self_failed")
                send_message(message_to, {"message_from": self.class_name}, message)
            else:
                message = self.get_prompt("execution_failed")
                send_message(message_to, {"message_from": self.class_name}, message)

    def find_variables(self, var_name):
        if self.context["variable_memory"] is None:
            return None
        for variable in self.context["variable_memory"]:
            if variable.name == var_name:
                return variable
        return None


