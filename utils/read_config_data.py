import yaml


def read_yaml_data(yaml_path):
    with open(yaml_path, "r", encoding="UTF-8") as fp:
        data = yaml.safe_load(fp)
    return data
