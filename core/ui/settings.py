from __future__ import annotations

import os
from typing import Callable, Dict, List, Optional

import customtkinter as ctk
import keyboard

from core.config import Config
from core.constants import (
    APP_NAME,
    APP_VERSION,
    DEFAULT_HOTKEYS,
    get_resource_path,
)
from core.i18n import SUPPORTED_LOCALES, set_locale, t
from core.tools.listener import HotkeyListener
from core.ui.contracts import CloseReason


class Theme:
    BG_MAIN = "#000000"
    BG_GROUP = "#1C1C1E"
    TITLE_COLOR = "#FFFFFF"
    LABEL_COLOR = "#FFFFFF"
    SECONDARY_COLOR = "#8E8E93"
    BUTTON_BG = "#2C2C2E"
    BUTTON_HOVER = "#3A3A3C"


class Layout:
    MIN_WIDTH = 420
    MIN_HEIGHT = 280
    PADDING_H = 24
    PADDING_V = 20
    GROUP_RADIUS = 12
    GROUP_GAP = 24
    ROW_PADDING = 14


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class SettingsWindow:
    def __init__(
        self,
        config: Config,
        listener: HotkeyListener,
        on_close: Optional[Callable[[CloseReason], None]] = None,
        on_language_changed: Optional[Callable[[], None]] = None,
    ) -> None:
        self._config = config
        self._listener = listener
        self._on_close_callback = on_close
        self._on_language_changed_callback = on_language_changed
        self._hotkey_buttons: Dict[str, ctk.CTkButton] = {}
        self._hotkey_values: Dict[str, str] = {}
        self._root = ctk.CTk()
        self._record_action_key: Optional[str] = None
        self._record_hook: Optional[object] = None

    @property
    def root(self) -> ctk.CTk:
        return self._root

    def is_alive(self) -> bool:
        try:
            return self._root.winfo_exists()
        except Exception:
            return False

    def focus_window(self) -> None:
        if not self.is_alive():
            return
        try:
            self._refresh_hotkeys_from_config()
            self._root.deiconify()
            self._root.lift()
            self._root.focus_force()
        except Exception:
            pass

    def request_destroy(self) -> None:
        if not self.is_alive():
            return
        try:
            self._root.after(0, lambda: self._close(CloseReason.DESTROYED))
        except Exception:
            pass

    def _close(self, reason: CloseReason) -> None:
        self._stop_recording()
        if self._on_close_callback:
            self._on_close_callback(reason)
        if not self.is_alive():
            return
        if reason is CloseReason.DESTROYED:
            try:
                self._root.quit()
            except Exception:
                pass
            try:
                self._root.destroy()
            except Exception:
                pass
        else:
            try:
                self._root.withdraw()
            except Exception:
                pass

    def _refresh_hotkeys_from_config(self) -> None:
        hotkeys = self._config.get_hotkeys()
        for key in DEFAULT_HOTKEYS:
            self._hotkey_values[key] = hotkeys.get(key, DEFAULT_HOTKEYS[key])
            btn = self._hotkey_buttons.get(key)
            if btn:
                btn.configure(
                    text=self._format_combo(self._hotkey_values[key])
                )

    def run(self) -> None:
        self._build_ui()
        self._root.protocol(
            "WM_DELETE_WINDOW",
            lambda: self._close(CloseReason.HIDDEN),
        )
        self._root.mainloop()

    def _build_ui(self) -> None:
        self._configure_root()
        main = ctk.CTkFrame(self._root, fg_color="transparent")
        main.pack(fill="both", expand=True)
        self._content_parent = main
        content = ctk.CTkFrame(main, fg_color=Theme.BG_MAIN, corner_radius=0)
        content.pack(fill="both", expand=True)
        self._build_header(content)
        self._build_hotkeys_block(content)
        self._build_language_block(content)
        self._build_version_block(content)
        self._apply_geometry()

    def _configure_root(self) -> None:
        self._root.title(APP_NAME)
        self._root.resizable(False, False)
        self._root.configure(fg_color=Theme.BG_MAIN)
        self._set_window_icon()

    def _set_window_icon(self) -> None:
        path = get_resource_path(os.path.join("assets", "icon.ico"))
        if os.path.isfile(path):
            try:
                self._root.iconbitmap(path)
            except Exception:
                pass

    def _build_header(self, parent: ctk.CTkFrame) -> None:
        ctk.CTkLabel(
            parent,
            text=t("settings.title"),
            font=ctk.CTkFont(family="Segoe UI Black", size=34),
            text_color=Theme.TITLE_COLOR,
        ).pack(anchor="w", padx=Layout.PADDING_H, pady=(Layout.PADDING_V + 8, 4))
        ctk.CTkLabel(
            parent,
            text=t("settings.hotkeys_section"),
            font=ctk.CTkFont(size=13),
            text_color=Theme.SECONDARY_COLOR,
        ).pack(anchor="w", padx=Layout.PADDING_H, pady=(8, 6))

    def _build_hotkeys_block(self, parent: ctk.CTkFrame) -> None:
        group = ctk.CTkFrame(
            parent,
            fg_color=Theme.BG_GROUP,
            corner_radius=Layout.GROUP_RADIUS,
        )
        group.pack(fill="x", padx=Layout.PADDING_H, pady=(0, Layout.GROUP_GAP))
        inner = ctk.CTkFrame(group, fg_color="transparent")
        inner.pack(fill="x", padx=16, pady=4)
        inner.grid_columnconfigure(1, weight=1)

        hotkeys = self._config.get_hotkeys()
        for row, (key, _) in enumerate(DEFAULT_HOTKEYS.items()):
            self._hotkey_values[key] = hotkeys.get(key, DEFAULT_HOTKEYS[key])
            self._build_hotkey_row(inner, row, key)

    def _build_hotkey_row(self, parent: ctk.CTkFrame, row: int, key: str) -> None:
        ctk.CTkLabel(
            parent,
            text=t(f"hotkeys.{key}"),
            font=ctk.CTkFont(size=17),
            text_color=Theme.LABEL_COLOR,
        ).grid(row=row, column=0, sticky="w", padx=(0, 16), pady=Layout.ROW_PADDING)
        btn = ctk.CTkButton(
            parent,
            text=self._format_combo(self._hotkey_values[key]),
            width=130,
            height=32,
            font=ctk.CTkFont(size=17),
            fg_color=Theme.BUTTON_BG,
            hover_color=Theme.BUTTON_HOVER,
            text_color=Theme.LABEL_COLOR,
            corner_radius=8,
            command=lambda k=key: self._start_record(k),
        )
        btn.grid(row=row, column=1, sticky="e", pady=Layout.ROW_PADDING)
        self._hotkey_buttons[key] = btn

    def _build_language_block(self, parent: ctk.CTkFrame) -> None:
        ctk.CTkLabel(
            parent,
            text=t("settings.general_section"),
            font=ctk.CTkFont(size=13),
            text_color=Theme.SECONDARY_COLOR,
        ).pack(anchor="w", padx=Layout.PADDING_H, pady=(Layout.GROUP_GAP, 6))

        group = ctk.CTkFrame(
            parent,
            fg_color=Theme.BG_GROUP,
            corner_radius=Layout.GROUP_RADIUS,
        )
        group.pack(fill="x", padx=Layout.PADDING_H, pady=(0, Layout.GROUP_GAP))
        inner = ctk.CTkFrame(group, fg_color="transparent")
        inner.pack(fill="x", padx=16, pady=Layout.ROW_PADDING)
        inner.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            inner,
            text=t("settings.language"),
            font=ctk.CTkFont(size=17),
            text_color=Theme.LABEL_COLOR,
        ).grid(row=0, column=0, sticky="w", padx=(0, 16))

        options = [t("lang.en"), t("lang.ru")]
        current = t(f"lang.{self._config.get_language()}")
        self._lang_var = ctk.StringVar(value=current)
        menu = ctk.CTkOptionMenu(
            inner,
            values=options,
            variable=self._lang_var,
            width=130,
            height=32,
            font=ctk.CTkFont(size=17),
            fg_color=Theme.BUTTON_BG,
            button_color=Theme.BUTTON_BG,
            button_hover_color=Theme.BUTTON_BG,
            dropdown_fg_color=Theme.BG_GROUP,
            text_color=Theme.LABEL_COLOR,
            corner_radius=8,
            command=self._on_language_changed,
        )
        menu.grid(row=0, column=1, sticky="e")

    def _on_language_changed(self, choice: str) -> None:
        for loc in SUPPORTED_LOCALES:
            if choice == t("lang." + loc, locale=loc):
                if loc != self._config.get_language():
                    self._config.set_language(loc)
                    set_locale(loc)
                    self._refresh_ui_language()
                    self._listener.reload()
                    if self._on_language_changed_callback:
                        self._on_language_changed_callback()
                break

    def _refresh_ui_language(self) -> None:
        if not self.is_alive():
            return
        for child in self._content_parent.winfo_children():
            child.destroy()
        content = ctk.CTkFrame(
            self._content_parent,
            fg_color=Theme.BG_MAIN,
            corner_radius=0,
        )
        content.pack(fill="both", expand=True)
        self._build_header(content)
        self._build_hotkeys_block(content)
        self._build_language_block(content)
        self._build_version_block(content)
        self._apply_geometry()
        self._root.title(APP_NAME)

    def _build_version_block(self, parent: ctk.CTkFrame) -> None:
        group = ctk.CTkFrame(
            parent,
            fg_color=Theme.BG_GROUP,
            corner_radius=Layout.GROUP_RADIUS,
        )
        group.pack(fill="x", padx=Layout.PADDING_H, pady=(0, Layout.PADDING_V + 12))
        inner = ctk.CTkFrame(group, fg_color="transparent")
        inner.pack(fill="x", padx=16, pady=Layout.ROW_PADDING)
        inner.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(
            inner,
            text=t("settings.version"),
            font=ctk.CTkFont(size=17),
            text_color=Theme.LABEL_COLOR,
        ).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(
            inner,
            text=APP_VERSION,
            font=ctk.CTkFont(size=17),
            text_color=Theme.SECONDARY_COLOR,
        ).grid(row=0, column=1, sticky="e")

    def _apply_geometry(self) -> None:
        self._root.update_idletasks()
        w = max(self._root.winfo_reqwidth(), Layout.MIN_WIDTH)
        h = max(self._root.winfo_reqheight(), Layout.MIN_HEIGHT)
        self._root.geometry(f"{w}x{h}")
        self._root.minsize(w, h)

    def _start_record(self, key: str) -> None:
        if self._record_hook is not None:
            return
        self._record_action_key = key

        def on_key(event: keyboard.KeyboardEvent) -> None:
            if self._record_action_key is None or event.event_type != "down":
                return
            mods = self._pressed_modifiers()
            name = (event.name or "").strip().lower()
            if not name or name in ("ctrl", "shift", "alt", "win"):
                return
            combo = "+".join(mods + [name]).lower()
            action_key = self._record_action_key
            self._stop_recording()
            if self.is_alive():
                self._root.after(0, lambda: self._apply_recorded_combo(action_key, combo))

        self._record_hook = keyboard.hook(on_key, suppress=False)

    def _pressed_modifiers(self) -> List[str]:
        result: List[str] = []
        for mod in ("ctrl", "shift", "alt", "win"):
            try:
                if keyboard.is_pressed(mod):
                    result.append(mod)
            except Exception:
                pass
        return result

    def _stop_recording(self) -> None:
        if self._record_hook is not None:
            try:
                keyboard.unhook(self._record_hook)
            except Exception:
                pass
            self._record_hook = None
        self._record_action_key = None

    def _apply_recorded_combo(self, key: str, combo: str) -> None:
        if not self.is_alive():
            return
        combo = combo.strip().lower()
        if not combo:
            return
        self._hotkey_values[key] = combo
        btn = self._hotkey_buttons.get(key)
        if btn:
            btn.configure(text=self._format_combo(combo))
        self._save_and_reload_hotkeys()

    def _save_and_reload_hotkeys(self) -> None:
        hotkeys = {
            k: (self._hotkey_values.get(k) or "").strip().lower() or DEFAULT_HOTKEYS[k]
            for k in DEFAULT_HOTKEYS
        }
        self._config.save_config(hotkeys)
        self._listener.reload()

    @staticmethod
    def _format_combo(combo: str) -> str:
        if not combo:
            return "—"
        return "+".join(p.capitalize() for p in combo.lower().split("+"))
