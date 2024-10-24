import os
from pathlib import Path

import yaml
import json
import pika

from tbot.utils.llm import chat_llm

def convert2dict(obj):
    return obj.to_dict()


task_abstraction_prompt_str = """
system_prompt: |
  你是一个善于总结任务的助手，对于给定的任务，需要将具体的任务抽象化，通用化。
  
  ### 工作流 ###
  1. 识别出任务中指代具体对象的元素。
  2. 使用抽象符号来表示这些具体元素。
  3. 将原任务中的具体元素替换为抽象符号并输出。
  
  ### 示例 ###
  对于任务：将文件夹 "D:\\Awork\\AI-agent\\rpa-test\\test"重新命名为为"666"。
  抽象为：将文件夹 A 重新命名为 B。

task_prompt: |
  请帮我抽象任务 {task}。
  
  ### 输出格式 ###
  请直接输出抽象之后的任务，而不需要任何解释。
"""


def task_abstraction(task):
    prompt = yaml.safe_load(task_abstraction_prompt_str)

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
