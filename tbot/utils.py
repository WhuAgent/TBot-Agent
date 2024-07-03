import os


def get_system_prompt():
    def add_action(prompt, action_file_path):
        prompt = f"{prompt}\n\n"
        with open(action_file_path, "r", encoding="UTF-8") as f:
            lines = f.readlines()
            for line in lines:
                prompt = f"{prompt}\t{line}"
        return prompt

    with open("prompt/tbot/system_prompt.txt", "r", encoding="UTF-8") as f:
        system_prompt = f.read()

    for root, dirs, files in os.walk("prompt/tbot/action"):
        for file in files:
            file_path = os.path.join(root, file)
            system_prompt = add_action(system_prompt, file_path)

    return system_prompt


def get_task_prompt(task):
    with open("prompt/tbot/task_prompt.txt", "r", encoding="UTF-8") as f:
        task_prompt = f.read()
        task_prompt = task_prompt.replace("{task}", task)
    return task_prompt
