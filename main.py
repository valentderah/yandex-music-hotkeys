from core.config import Config
from core.controller import MediaController
from core.listener import HotkeyListener
from core.tray import TrayIcon


def main() -> None:
    config = Config()
    controller = MediaController()
    listener = HotkeyListener(controller, config)

    listener.start()

    tray = TrayIcon(listener, config)
    tray.run()


if __name__ == "__main__":
    main()
