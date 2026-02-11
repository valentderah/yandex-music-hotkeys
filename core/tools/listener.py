import keyboard
from typing import Dict, Callable, Set, Optional, Tuple

from core.tools.controller import MediaController
from core.config import Config

_MODIFIERS: Tuple[str, ...] = ("ctrl", "shift", "alt", "win")


class HotkeyListener:
    def __init__(self, controller: MediaController, config: Config) -> None:
        self.controller = controller
        self.config = config
        self._hotkeys: Dict[str, Callable[[], None]] = {}
        self._pressed_keys: Set[str] = set()
        self._hook_handle: Optional[object] = None

    def on_next(self) -> None:
        self.controller.next_track()

    def on_previous(self) -> None:
        self.controller.previous_track()

    def on_play_pause(self) -> None:
        self.controller.play_pause()

    def _build_hotkey_map(self) -> None:
        self._hotkeys.clear()
        hotkeys_config = self.config.get_hotkeys()
        action_map: Dict[str, Callable[[], None]] = {
            "next_track": self.on_next,
            "previous_track": self.on_previous,
            "play_pause": self.on_play_pause,
        }
        for action, combo in hotkeys_config.items():
            if combo and action in action_map:
                self._hotkeys[combo.lower()] = action_map[action]

    def _on_key_event(self, event: keyboard.KeyboardEvent) -> bool:
        key_name = (event.name or "").strip().lower()
        if not key_name:
            return True

        if event.event_type == keyboard.KEY_UP:
            self._pressed_keys.discard(key_name)
            return True

        self._pressed_keys.add(key_name)
        if key_name in _MODIFIERS:
            return True

        mods = [m for m in _MODIFIERS if m in self._pressed_keys]
        current_combo = "+".join(mods + [key_name])
        callback = self._hotkeys.get(current_combo)
        if callback:
            callback()
            return False
        return True

    def apply_hotkeys(self) -> None:
        self.stop()
        self._build_hotkey_map()
        if self._hotkeys:
            self._hook_handle = keyboard.hook(self._on_key_event)

    def start(self) -> None:
        self.apply_hotkeys()

    def stop(self) -> None:
        if self._hook_handle:
            try:
                keyboard.unhook(self._hook_handle)
            except Exception:
                pass
            self._hook_handle = None
        self._pressed_keys.clear()

    def reload(self) -> None:
        self.apply_hotkeys()
