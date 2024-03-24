import json
from typing import Any, Dict

from config.configuration import SETTINGS_PATH
from utils.event import Event


class SettingsReader:
    def __init__(self) -> None:
        with open(SETTINGS_PATH, 'r') as f:
            self.settings = json.load(f)

    def get_value(self, key: str) -> Any:
        return self.settings[key]

    def write_settings(self, new_settings: Dict[str, Any]) -> None:
        with open(SETTINGS_PATH, 'w') as f:
            json.dump(new_settings, f)

    def get_settings(self) -> Dict[str, Any]:
        return self.settings
