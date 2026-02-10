import os
import sys
from typing import Dict

APP_NAME = "YandexMusicHotkeys"
APP_VERSION = "0.9.0"

CONFIG_FILENAME = "config.json"

TARGET_WINDOW_TITLES = ["Yandex Music", "Яндекс Музыка"]

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