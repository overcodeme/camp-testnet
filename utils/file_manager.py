import json
import os
import yaml


def load_txt(file_path):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            pass
    else:
        with open(file_path, 'r') as file:
            data = [line.split()[0] for line in file.readlines()]
            return data


def save_wallet_session_data(wallet_address, key, value, file_path='config.yaml'):
    data = load_json(file_path)
    with open(file_path, 'w') as file:
        data[wallet_address][key] = value
        json.dump(data, file, indent=4)


def load_json(file_path):
    if not os.path.exists(file_path):
        return {}
    with open(file_path, 'r') as file:
        return json.load(file)


def load_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
        return data