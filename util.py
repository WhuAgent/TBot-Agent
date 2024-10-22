import os
from pathlib import Path

import yaml
import json
import pika

from tbot.utils.llm import chat_llm

def convert2dict(obj):
    return obj.to_dict()


def task_abstraction(task):
    prompt_path = "tbot/prompt/task_abstraction_agent.yaml"
    with open(prompt_path, "r", encoding="UTF-8") as f:
        prompt = yaml.safe_load(f)

    prompt["task_prompt"] = prompt["task_prompt"].replace("{task}", task)

    messages = [
        {"role": "system", "content": prompt["system_prompt"]},
        {"role": "user", "content": prompt["task_prompt"]},
    ]

    model = "gpt-3.5-turbo"

    response = chat_llm(model, messages)

    return response.content

def get_action_configs(action_config_path):
    action_configs = {}
    for root, dirs, files in os.walk(action_config_path):
        for file in files:
            if file.endswith(".prompt"):
                action_name = file[:-7]
                file_path = Path(os.path.join(root, file))
                action_path = "/".join(file_path.parts)
                action_module = ".".join(file_path.parts)[:-7]
                action_configs.update({action_name: {
                    "prompt_path": action_path,
                    "action_module": action_module
                }})
    return action_configs

def decorate_message(message, **kwargs):
    for key, value in kwargs.items():
        origin = "{" + key + "}"
        if type(value) == str:
            message = message.replace(origin, value)
        else:
            message = message.replace(origin, json.dumps(value, indent=4, ensure_ascii=False, default=convert2dict))
    return message


def send_message(target: str, header, message):
    exchange = target + "Exchange"
    routing_key = target

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, exchange_type='direct')
    channel.queue_declare(queue=routing_key, durable=True)
    channel.queue_bind(exchange=exchange, queue=routing_key, routing_key=routing_key)

    properties = pika.BasicProperties(headers=header)
    channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message, properties=properties)
    # print(f"Sent: {message}")
    connection.close()
