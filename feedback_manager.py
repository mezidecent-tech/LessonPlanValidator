import json


def load_feedback():

    with open("feedback/comments.json", "r", encoding="utf-8") as file:

        return json.load(file)