import click
import os
import json

import yaml

from model.utils import chat_llm
from model.agent import MiniWobAgent, parse_action
from model.utils import get_tasks, read_yaml


def action2func_call(action):
    def format_dict_item(key, value):
        return f"{key}: {value}"

    def format_arg(key, value):
        if isinstance(value, str):
            return f'{key}="{value}"'
        elif isinstance(value, dict):
            formatted_items = ", ".join([format_dict_item(k, v) for k, v in value.items()])
            return f'{key}={{ {formatted_items} }}'
        else:
            return f'{key}={value}'

    func_name = action.get("action")
    args = action.get("args")
    args_str = ", ".join([format_arg(k, v) for k, v in args.items()]) if args else ""
    func_str = f"{func_name}({args_str})"
    return func_str


def generate_action(model, messages, task, last_action, observation, plan, history_action):
    with open("prompt/step_prompt.txt", "r", encoding="UTF-8") as f:
        prompt = f.read()
    prompt = prompt.replace("{task}", task)

    if not last_action:
        prompt = prompt.replace("{action}", "")
    else:
        func_str = action2func_call(last_action)
        prompt = prompt.replace("{action}", f"刚刚进行了动作：{func_str}\n\n")

    prompt = prompt.replace("{observation}", observation)
    prompt = prompt.replace("{plan}", plan)
    prompt = prompt.replace("{history_action}", json.dumps(history_action, indent=4))

    messages.append({"role": "user", "content": prompt})
    agent.log(f"user:\n{prompt}")

    response = chat_llm(model, messages)
    agent.log(f"{response.role}:\n{response.content}")
    messages.append({"role": response.role, "content": response.content})
    action = parse_action(response.content)
    return action, messages


if __name__ == '__main__':
    # env_name = "click-shades"
    task_config_path = os.path.join(os.path.dirname(__file__), "../config/miniwob_tasks.yaml")
    task_data = read_yaml(task_config_path)
    tasks = task_data["miniwob_tasks"]
    # tasks = ["click-shades"]

    succeed_envs_path = os.path.join(os.path.dirname(__file__), "../config/succeed_envs.yaml")
    succeed_envs = read_yaml(succeed_envs_path)

    for task in tasks:
        if task in succeed_envs:
            continue
        env_name = task
        print()
        print(f"{env_name}: ")
        for _ in range(10):
            if _ == 5:
                middle = 1
            print(_, end=" ")
            agent = MiniWobAgent(env_name, logger_prefix="debug_test")

            model = "gpt-3.5-turbo"
            messages = [
                {"role": "system", "content": agent.system_prompt},
                {"role": "user", "content": agent.task_prompt}
            ]

            for message in messages:
                agent.log(f"{message['role']}:\n{message['content']}")

            click.echo(click.style(agent.task, fg="green"))
            response = chat_llm(model, messages)
            messages.append({"role": response.role, "content": response.content})
            agent.plan = response.content

            agent.log(f"{response.role}:\n{agent.plan}")

            last_action = None

            html_description, form_data_status = agent.obs()
            html_description = json.dumps(html_description, indent=4)
            form_data_status = json.dumps(form_data_status, indent=4)
            observation = f"页面中包含的元素：\n\n{html_description}\n\n页面中的表单数据：\n\n{form_data_status}"
            reward = -1

            try:
                for _ in range(20):
                    action, messages = generate_action(model,
                                                       messages,
                                                       agent.task,
                                                       last_action,
                                                       observation,
                                                       agent.plan,
                                                       agent.history_action)
                    observation, reward, done, info = agent.step(action)
                    last_action = action
                    agent.history_action.append(last_action)
                    if done:
                        agent.log(f"reward: {reward}")
                        agent.log(f"info: {info}")
                        break
            except Exception as e:
                agent.log(f"error: {type(e)} {e}")

            agent.logger.rename(reward > 0)

            agent.log("进行的动作总结：")
            for action in agent.history_action:
                agent.log(f"{action2func_call(action)}")

        succeed_envs.append(task)
        with open(succeed_envs_path, "w", encoding="UTF-8") as f:
            yaml.dump(succeed_envs, f, allow_unicode=True, default_flow_style=False)
