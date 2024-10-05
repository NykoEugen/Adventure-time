import json
import os


def initialize_json(file_path, initial_data=None):
    if os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump(initial_data if initial_data else {}, f)
    else:
        with open(file_path, 'w') as f:
            json.dump(initial_data if initial_data else {}, f)

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        texts = json.load(file)
    return texts

def save_json(data, file_path="text-templates/game-context.json"):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)