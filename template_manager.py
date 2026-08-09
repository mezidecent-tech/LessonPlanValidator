import json


def load_template(template_name):

    file_path = f"config/{template_name}.json"

    with open(file_path, "r", encoding="utf-8") as file:

        template = json.load(file)

    return template