from __future__ import annotations

from typing import Dict

SUPPORTED_LOCALES = ("en", "ru")
DEFAULT_LOCALE = "en"

_TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "en": {
        "menu.open_app": "Open Yandex Music",
        "menu.settings": "Settings",
        "menu.exit": "Exit",
        "window.settings_title": "Settings",
        "settings.title": "Settings",
        "settings.hotkeys_section": "HOTKEYS",
        "settings.general_section": "GENERAL",
        "settings.language": "Language",
        "settings.autostart": "Run at startup",
        "settings.version": "Version",
        "hotkeys.next_track": "Next track",
        "hotkeys.previous_track": "Previous track",
        "hotkeys.play_pause": "Play/Pause",
        "lang.en": "English",
        "lang.ru": "Русский",
    },
    "ru": {
        "menu.open_app": "Открыть Яндекс Музыку",
        "menu.settings": "Настройки",
        "menu.exit": "Закрыть",
        "window.settings_title": "Настройки",
        "settings.title": "Настройки",
        "settings.hotkeys_section": "ГОРЯЧИЕ КЛАВИШИ",
        "settings.general_section": "ОБЩИЕ",
        "settings.language": "Язык",
        "settings.autostart": "Автозагрузка приложения",
        "settings.version": "Версия",
        "hotkeys.next_track": "Следующий трек",
        "hotkeys.previous_track": "Предыдущий трек",
        "hotkeys.play_pause": "Воспроизведение/Пауза",
        "lang.en": "English",
        "lang.ru": "Русский",
    },
}

_current_locale: str = DEFAULT_LOCALE


def set_locale(locale: str) -> None:
    global _current_locale
    _current_locale = locale if locale in SUPPORTED_LOCALES else DEFAULT_LOCALE


def get_locale() -> str:
    return _current_locale


def t(key: str, locale: str | None = None) -> str:
    loc = locale if locale is not None and locale in SUPPORTED_LOCALES else _current_locale
    table = _TRANSLATIONS.get(loc, _TRANSLATIONS[DEFAULT_LOCALE])
    return table.get(key, _TRANSLATIONS[DEFAULT_LOCALE].get(key, key))
