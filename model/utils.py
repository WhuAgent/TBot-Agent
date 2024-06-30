import json
import os
import yaml

from openai import OpenAI
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def read_yaml(yaml_path):
    with open(yaml_path, "r", encoding="UTF-8") as fp:
        data = yaml.safe_load(fp)
    return data


def get_tasks(root):
    items = os.listdir(root)

    # 一个 folder 就是一个 task
    folders = [item for item in items if os.path.isdir(os.path.join(root, item))]
    folders.sort()
    if "webshop" in folders:
        folders.remove("webshop")
    return folders


def get_webdriver():
    args = read_yaml("config/config.yaml")
    service = Service(args["chromedriver_path"])
    options = webdriver.ChromeOptions()
    options.add_argument("disable-gpu")
    options.add_argument("no-sandbox")

    chromedriver = webdriver.Chrome(service=service, options=options)
    chromedriver.implicitly_wait(5)
    chromedriver.maximize_window()
    chromedriver.implicitly_wait(5)

    return chromedriver


def html_status2description(html_status):
    html_description = {k: html_status[k] for k in html_status.keys()}
    remove_field(html_description, ["path", "element"])
    return html_description


def remove_field(obj, fields_to_remove):
    if isinstance(obj, dict):
        for key in list(obj.keys()):
            if key in fields_to_remove:
                obj.pop(key)
            else:
                remove_field(obj[key], fields_to_remove)
    elif isinstance(obj, list):
        for item in obj:
            remove_field(item, fields_to_remove)


def get_prompts(task, html_description, form_data_status):
    def add_action(prompt, action_file_path):
        prompt = f"{prompt}\n\n"
        with open(action_file_path, "r", encoding="UTF-8") as f:
            lines = f.readlines()
            for line in lines:
                prompt = f"{prompt}\t{line}"
        return prompt

    with open("prompt/system_prompt.txt", "r", encoding="UTF-8") as f:
        system_prompt = f.read()

    for root, dirs, files in os.walk("prompt/action"):
        for file in files:
            file_path = os.path.join(root, file)
            system_prompt = add_action(system_prompt, file_path)

    with open("prompt/task_prompt.txt", "r", encoding="UTF-8") as f:
        task_prompt = f.read()
        task_prompt = task_prompt.replace("{task}", task)
        task_prompt = task_prompt.replace("{html_description}", json.dumps(html_description, indent=4))
        task_prompt = task_prompt.replace("{form_data_status}", json.dumps(form_data_status, indent=4))

    return system_prompt, task_prompt


openai_config_path = os.path.join(os.path.dirname(__file__), "..", "config", "openai_config.yaml")
openai_config = read_yaml(openai_config_path)


def llm(model, prompt, stop=None):
    if stop is None:
        stop = ["\n"]

    openai_client = OpenAI(
        api_key=openai_config["api_key"],
        base_url=openai_config["base_url"]
    )
    response = openai_client.completions.create(
        model=model,
        prompt=prompt,
        temperature=0,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=stop
    )
    return response.choices[0].text


def chat_llm(model, messages):
    openai_client = OpenAI(
        api_key=openai_config["api_key"],
        base_url=openai_config["base_url"]
    )
    response = openai_client.chat.completions.create(
        messages=messages,
        model=model
    )
    return response.choices[0].message
