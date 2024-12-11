import json
import os
from datetime import datetime


class Config:
    _instance = None
    values = [
        {"name": "Path to questions", "value": "QUESTIONS_PATH"},
        {"name": "Path to responses result", "value": "RESPONSES_PATH"},
    ]

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.config_file_path = "resources/config.json"
        self.config = self.init_configs()

    def init_configs(self):
        config = {}
        if not os.path.exists(self.config_file_path):
            with open(self.config_file_path, "w") as f:
                json.dump({item["value"]: "" for item in Config.values}, f)
        else:
            with open(self.config_file_path, "r") as f:
                config = json.load(f)

            for item in Config.values:
                if item["value"] not in config:
                    config[item["value"]] = input(f"Enter value for '{item['name']}': ")

            with open(self.config_file_path, "w") as f:
                json.dump(config, f)
        return config

    def get_questions_path(self):
        return self.config.get("QUESTIONS_PATH", None)

    def get_responses_path(self):
        return self.config.get("RESPONSES_PATH", None)

