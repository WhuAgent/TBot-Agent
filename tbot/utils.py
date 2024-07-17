import os
import yaml

prompt_path = "prompt/tbot.yaml"
with open(prompt_path, "r", encoding="utf-8") as f:
    prompt = yaml.safe_load(f)


def get_system_prompt():
    def add_action(prompt, action_file_path):
        prompt = f"{prompt}\n\n"
        with open(action_file_path, "r", encoding="UTF-8") as f:
            lines = f.readlines()
            for line in lines:
                prompt = f"{prompt}\t{line}"
        return prompt

    system_prompt = prompt["system_prompt"]

    for root, dirs, files in os.walk("config/actions"):
        for file in files:
            if file.endswith(".prompt"):
                file_path = os.path.join(root, file)
                system_prompt = add_action(system_prompt, file_path)

    return system_prompt


def get_task_prompt(task):
    task_prompt = prompt["task_prompt"]
    task_prompt = task_prompt.replace("{task}", task)
    return task_prompt
