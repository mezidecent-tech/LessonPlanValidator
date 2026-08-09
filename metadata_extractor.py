import json
import re


def load_aliases():
    with open("config/metadata_aliases.json", "r", encoding="utf-8") as file:
        return json.load(file)


def extract_metadata(text):

    aliases = load_aliases()
    metadata = {}

    # Split the document into individual lines
    lines = text.splitlines()

    for field, names in aliases.items():

        metadata[field] = "Not Found"

        for line in lines:

            line = line.strip()

            for name in names:

                pattern = rf"^{re.escape(name)}\s*[:=-]\s*(.+)$"

                match = re.match(pattern, line, re.IGNORECASE)

                if match:
                    metadata[field] = match.group(1).strip()
                    break

            if metadata[field] != "Not Found":
                break

    return metadata