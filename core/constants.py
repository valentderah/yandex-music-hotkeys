import os
import sys
from typing import Dict

APP_NAME = "Yandex Music Hotkeys"
APP_VERSION = "1.0.0"
APP_OWNER = "Valiantsin Dzerakh"
OWNER_TAGNAME = "valentderah"

CONFIG_FILENAME = "config.json"

TARGET_WINDOW_TITLES = ["Yandex Music", "Яндекс Музыка"]

YANDEX_MUSIC_PROTOCOL = "yandexmusic://"
REGISTRY_RUN_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"

DEFAULT_HOTKEYS: Dict[str, str] = {
    "next_track": "ctrl+right",
    "previous_track": "ctrl+left",
    "play_pause": "ctrl+space",
}

WM_APPCOMMAND = 0x0319

APPCOMMAND_MEDIA_NEXTTRACK = 11
APPCOMMAND_MEDIA_PREVIOUSTRACK = 12
APPCOMMAND_MEDIA_PLAY_PAUSE = 14


def get_resource_path(relative_path: str) -> str:
    try:
        base_path = sys._MEIPASS  # type: ignore[attr-defined]
    except AttributeError:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
