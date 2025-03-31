import json
import os

def load_json(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Config file not found: {file_path}")
    with open(file_path, 'r') as f:
        return json.load(f)

def load_all_configs():
    return {
        "test_data": load_json("web/fixtures/test_data.json"),
        "config_e2e": load_json("web/config.json"),

    }
