from __future__ import annotations

import os
import pystray
import threading
from PIL import Image
from typing import Optional, TYPE_CHECKING

from core.listener import HotkeyListener
from core.config import Config
from core.constants import APP_NAME, get_resource_path

if TYPE_CHECKING:
    from core.gui import SettingsWindow


def _enable_dark_menu() -> None:
    try:
        import ctypes
        uxtheme = ctypes.WinDLL("uxtheme")
        # SetPreferredAppMode (ordinal 135): 2 = ForceDark
        set_mode = uxtheme[135]
        set_mode.argtypes = [ctypes.c_int]
        set_mode.restype = ctypes.c_int
        set_mode(2)
        # FlushMenuThemes (ordinal 136)
        flush = uxtheme[136]
        flush.argtypes = []
        flush.restype = None
        flush()
    except Exception:
        pass


class TrayIcon:
    def __init__(self, listener: HotkeyListener, config: Config) -> None:
        self.listener = listener
        self.config = config
        self.icon: Optional[pystray.Icon] = None
        self._settings_window: Optional[SettingsWindow] = None
        self._settings_lock = threading.Lock()

    def create_image(self) -> Image.Image:
        icon_path = get_resource_path(os.path.join("assets", "icon.ico"))
        if os.path.isfile(icon_path):
            return Image.open(icon_path)
        size = 64
        return Image.new("RGBA", (size, size), (88, 166, 255, 255))

    def on_settings(self, icon: pystray.Icon, _item: pystray.MenuItem) -> None:
        if not self._settings_lock.acquire(blocking=False):
            return
        try:
            if self._settings_window is not None:
                return

            self.listener.stop()

            from core.gui import SettingsWindow

            window = SettingsWindow(self.config, self.listener)
            self._settings_window = window
            window.run()
        finally:
            self._settings_window = None
            self.listener.reload()
            self._settings_lock.release()

    def on_reload(self, icon: pystray.Icon, _item: pystray.MenuItem) -> None:
        self.listener.reload()

    def on_exit(self, icon: pystray.Icon, _item: pystray.MenuItem) -> None:
        window = self._settings_window
        if window is not None:
            window.request_close()
        self.listener.stop()
        icon.stop()

    def run(self) -> None:
        _enable_dark_menu()
        menu = pystray.Menu(
            pystray.MenuItem("Settings", self.on_settings, default=True),
            pystray.MenuItem("Reload Config", self.on_reload),
            pystray.MenuItem("Exit", self.on_exit),
        )
        self.icon = pystray.Icon(
            "yandex_music_hotkeys",
            self.create_image(),
            APP_NAME,
            menu,
        )
        self.icon.run()
