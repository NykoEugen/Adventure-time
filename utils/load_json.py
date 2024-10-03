import json


def load_texts(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        texts = json.load(file)
    return texts