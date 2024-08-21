import os
from pathlib import Path

import yaml

from utils.llm import chat_llm


def add_relevant_actions_prompt(relevant_commands, action_config):
    def add_action(prompt, action_file_path):
        prompt = f"{prompt}\n\n"
        with open(action_file_path, "r", encoding="UTF-8") as f:
            lines = f.readlines()
            for line in lines:
                prompt = f"{prompt}{line}"
        return prompt

    relevant_actions_prompt = ""

    for command in relevant_commands:
        relevant_actions_prompt = add_action(relevant_actions_prompt, action_config[command]["prompt_path"])

    return relevant_actions_prompt[2:]


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


def task_abstraction(task):
    prompt_path = "prompt/task_abstraction_agent.yaml"
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
