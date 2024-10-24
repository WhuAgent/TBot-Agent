import os
from tbot.utils.read_config_data import read_yaml_data

from openai import OpenAI

# openai_config_path = os.path.join(os.path.dirname(__file__), "..", "config", "openai_config.yaml")
openai_config_path = "tbot/config/openai.yml"
openai_config = read_yaml_data(openai_config_path)


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
