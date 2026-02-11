from enum import Enum
from typing import Protocol, runtime_checkable


class CloseReason(str, Enum):
    HIDDEN = "hidden"
    DESTROYED = "destroyed"


@runtime_checkable
class SettingsWindowProtocol(Protocol):
    def focus_window(self) -> None: ...
    def request_destroy(self) -> None: ...
