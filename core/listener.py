import keyboard
from typing import List, Dict, Callable

from core.controller import MediaController
from core.config import Config


class HotkeyListener:
    def __init__(self, controller: MediaController, config: Config) -> None:
        self.controller = controller
        self.config = config
        self.hook_handles: List[object] = []

    def on_next(self) -> None:
        self.controller.next_track()

    def on_previous(self) -> None:
        self.controller.previous_track()

    def on_play_pause(self) -> None:
        self.controller.play_pause()

    def apply_hotkeys(self) -> None:
        self.stop()

        hotkeys_config = self.config.get_hotkeys()
        
        action_map: Dict[str, Callable[[], None]] = {
            "next_track": self.on_next,
            "previous_track": self.on_previous,
            "play_pause": self.on_play_pause,
        }

        for action, combo in hotkeys_config.items():
            if not combo or action not in action_map:
                continue
            try:
                handle = keyboard.add_hotkey(combo, action_map[action], suppress=True)
                self.hook_handles.append(handle)
            except Exception:
                pass

    def start(self) -> None:
        self.apply_hotkeys()

    def stop(self) -> None:
        for handle in self.hook_handles:
            try:
                keyboard.unhook(handle)
            except Exception:
                pass
        self.hook_handles.clear()

    def reload(self) -> None:
        self.apply_hotkeys()
