from core.config import Config
from core.i18n import set_locale
from core.tools.controller import MediaController
from core.tools.listener import HotkeyListener
from core.ui.tray import TrayIcon


def main() -> None:
    config = Config()
    set_locale(config.get_language())

    controller = MediaController()
    listener = HotkeyListener(controller, config)
    listener.start()

    tray = TrayIcon(listener, config)
    tray.run()


if __name__ == "__main__":
    main()
