from __future__ import annotations

import os
import threading
import webbrowser
from typing import Optional, TYPE_CHECKING

import pystray
from PIL import Image

from core.config import Config
from core.constants import APP_NAME, YANDEX_MUSIC_PROTOCOL, get_resource_path
from core.i18n import t
from core.tools.listener import HotkeyListener
from core.ui.contracts import CloseReason

if TYPE_CHECKING:
    from core.ui.settings import SettingsWindow


def _enable_dark_tray_menu() -> None:
    try:
        import ctypes
        uxtheme = ctypes.WinDLL("uxtheme")
        set_mode = uxtheme[135]
        set_mode.argtypes = [ctypes.c_int]
        set_mode.restype = ctypes.c_int
        set_mode(2)
        flush = uxtheme[136]
        flush.argtypes = []
        flush.restype = None
        flush()
    except Exception:
        pass


def _load_tray_icon() -> Image.Image:
    path = get_resource_path(os.path.join("assets", "icon.ico"))
    if os.path.isfile(path):
        return Image.open(path)
    return Image.new("RGBA", (64, 64), (88, 166, 255, 255))


class TrayIcon:
    def __init__(self, listener: HotkeyListener, config: Config) -> None:
        self._listener = listener
        self._config = config
        self._icon: Optional[pystray.Icon] = None
        self._settings_window: Optional[SettingsWindow] = None
        self._settings_lock = threading.Lock()

    def run(self) -> None:
        _enable_dark_tray_menu()
        menu = pystray.Menu(
            pystray.MenuItem(
                lambda _: "",
                self._on_settings_click,
                default=True,
                visible=False,
            ),
            pystray.MenuItem(
                lambda _: t("menu.open_app"),
                self._on_open_app_click,
            ),
            pystray.MenuItem(
                lambda _: t("menu.settings"),
                self._on_settings_click,
            ),
            pystray.MenuItem(lambda _: t("menu.exit"), self._on_exit_click),
        )
        self._icon = pystray.Icon(
            "yandex_music_hotkeys",
            _load_tray_icon(),
            APP_NAME,
            menu,
        )
        self._icon.run(setup=self._on_tray_ready)

    def _on_tray_ready(self, icon: pystray.Icon) -> None:
        icon.visible = True
        self._listener.reload()

    def _on_language_changed(self) -> None:
        if self._icon is not None:
            try:
                self._icon.update_menu()
            except Exception:
                pass

    def _on_open_app_click(
        self,
        _icon: pystray.Icon,
        _item: pystray.MenuItem,
    ) -> None:
        webbrowser.open(YANDEX_MUSIC_PROTOCOL)

    def _on_settings_click(
        self,
        _icon: pystray.Icon,
        _item: pystray.MenuItem,
    ) -> None:
        if self._settings_window is not None:
            self._settings_window.focus_window()
            return
        if not self._settings_lock.acquire(blocking=False):
            return
        threading.Thread(target=self._run_settings_ui, daemon=True).start()


    def _on_exit_click(
        self,
        icon: pystray.Icon,
        _item: pystray.MenuItem,
    ) -> None:
        if self._settings_window is not None:
            self._settings_window.request_destroy()
            self._settings_window = None
        self._listener.stop()
        icon.stop()

    def _run_settings_ui(self) -> None:
        from core.ui.settings import SettingsWindow

        # self._listener.stop()
        window = SettingsWindow(
            self._config,
            self._listener,
            on_close=self._when_settings_closed,
            on_language_changed=self._on_language_changed,
        )
        self._settings_window = window
        try:
            window.run()
        finally:
            self._when_settings_closed(CloseReason.DESTROYED)

    def _when_settings_closed(self, reason: CloseReason) -> None:
        if reason is CloseReason.DESTROYED:
            self._settings_window = None
        try:
            self._settings_lock.release()
        except RuntimeError:
            pass
        self._listener.reload()
