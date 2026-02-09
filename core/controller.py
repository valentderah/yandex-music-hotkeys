import ctypes
from ctypes import wintypes
from typing import Optional, List

from core.constants import (
    WM_APPCOMMAND,
    APPCOMMAND_MEDIA_NEXTTRACK,
    APPCOMMAND_MEDIA_PREVIOUSTRACK,
    APPCOMMAND_MEDIA_PLAY_PAUSE,
    TARGET_WINDOW_TITLES
)


class MediaController:
    def __init__(self) -> None:
        self.user32 = ctypes.windll.user32
        self.enum_results: List[int] = []

    def enum_callback(self, hwnd: int, _lparam: int) -> int:
        length = self.user32.GetWindowTextLengthW(hwnd) + 1
        buf = ctypes.create_unicode_buffer(length)
        self.user32.GetWindowTextW(hwnd, buf, length)
        title = buf.value or ""
        
        if any(target in title for target in TARGET_WINDOW_TITLES):
            self.enum_results.append(hwnd)
        return 1

    def find_yandex_music_window(self) -> Optional[int]:
        self.enum_results = []
        WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
        self.user32.EnumWindows(WNDENUMPROC(self.enum_callback), 0)
        return self.enum_results[0] if self.enum_results else None

    def send_command(self, hwnd: int, cmd: int) -> bool:
        if not hwnd or not self.user32.IsWindow(hwnd):
            return False
        return self.user32.SendMessageW(hwnd, WM_APPCOMMAND, hwnd, cmd << 16) != 0

    def send_media_key(self, cmd: int) -> bool:
        hwnd = self.find_yandex_music_window()
        return self.send_command(hwnd, cmd) if hwnd else False

    def next_track(self) -> bool:
        return self.send_media_key(APPCOMMAND_MEDIA_NEXTTRACK)

    def previous_track(self) -> bool:
        return self.send_media_key(APPCOMMAND_MEDIA_PREVIOUSTRACK)

    def play_pause(self) -> bool:
        return self.send_media_key(APPCOMMAND_MEDIA_PLAY_PAUSE)
