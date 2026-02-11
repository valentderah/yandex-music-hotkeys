import json
import locale
import os
import sys
from typing import Any, Dict

from core.constants import APP_NAME, CONFIG_FILENAME, DEFAULT_HOTKEYS
from core.i18n import DEFAULT_LOCALE, SUPPORTED_LOCALES


def _default_language() -> str:
    try:
        lang, _ = locale.getdefaultlocale() or (None, None)
        if lang and "ru" in (lang or "").lower():
            return "ru"
    except Exception:
        pass
    return DEFAULT_LOCALE


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
            default = {"hotkeys": dict(DEFAULT_HOTKEYS), "language": _default_language()}
            self._write_config(default)
            return default

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            return {"hotkeys": dict(DEFAULT_HOTKEYS), "language": _default_language()}

        hotkeys = data.get("hotkeys") or {}
        merged = dict(DEFAULT_HOTKEYS)
        for key in DEFAULT_HOTKEYS:
            if key in hotkeys and hotkeys[key]:
                merged[key] = str(hotkeys[key]).strip().lower()

        lang = data.get("language") or _default_language()
        if lang not in SUPPORTED_LOCALES:
            lang = DEFAULT_LOCALE

        return {"hotkeys": merged, "language": lang}

    def _write_config(self, data: Dict[str, Any]) -> None:
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except OSError:
            pass

    def save_default_config(self) -> None:
        self._write_config({
            "hotkeys": dict(DEFAULT_HOTKEYS),
            "language": self.get_language(),
        })

    def get_hotkeys(self) -> Dict[str, str]:
        return self.load_config().get("hotkeys", dict(DEFAULT_HOTKEYS))

    def get_language(self) -> str:
        return self.load_config().get("language", _default_language())

    def set_language(self, lang: str) -> None:
        if lang not in SUPPORTED_LOCALES:
            lang = DEFAULT_LOCALE
        data = self.load_config()
        data["language"] = lang
        self._write_config(data)

    def save_config(self, hotkeys: Dict[str, str]) -> None:
        data = self.load_config()
        data["hotkeys"] = hotkeys
        self._write_config(data)
