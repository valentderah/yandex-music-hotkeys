import json
import os
import sys
from typing import Dict, Any

from core.constants import APP_NAME, CONFIG_FILENAME, DEFAULT_HOTKEYS


class Config:
    def __init__(self) -> None:
        self.config_path = self.get_config_path()

    def get_config_path(self) -> str:
        return os.path.join(self.get_app_data_path(), CONFIG_FILENAME)

    @staticmethod
    def get_app_data_path() -> str:
        if sys.platform == "win32":
            base_path = os.getenv("LOCALAPPDATA") or os.path.expanduser("~\\AppData\\Local")
        else:
            base_path = os.path.join(os.path.expanduser("~"), ".config")
        
        path = os.path.join(base_path, APP_NAME)
        os.makedirs(path, exist_ok=True)
        return path

    def load_config(self) -> Dict[str, Any]:
        if not os.path.isfile(self.config_path):
            self.save_default_config()
            return {"hotkeys": dict(DEFAULT_HOTKEYS)}

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            return {"hotkeys": dict(DEFAULT_HOTKEYS)}

        hotkeys = data.get("hotkeys") or {}

        merged = dict(DEFAULT_HOTKEYS)
        for key in DEFAULT_HOTKEYS:
            if key in hotkeys and hotkeys[key]:
                merged[key] = str(hotkeys[key]).strip().lower()
        
        return {"hotkeys": merged}

    def save_default_config(self) -> None:
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump({"hotkeys": DEFAULT_HOTKEYS}, f, indent=2)
        except OSError:
            pass

    def get_hotkeys(self) -> Dict[str, str]:
        return self.load_config().get("hotkeys", dict(DEFAULT_HOTKEYS))

    def save_config(self, hotkeys: Dict[str, str]) -> None:
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump({"hotkeys": hotkeys}, f, indent=2)
        except OSError:
            pass
