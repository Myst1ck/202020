from typing import Tuple
from PIL import Image
from pystray import MenuItem, Icon
from pystray._win32 import Icon as icon

from config.configuration import ICON_PATH
from utils.event import Event


class TrayIcon:
    def __init__(self, on_start: Event, on_exit: Event) -> None:
        self.on_window_show: Event = Event()
        self.on_window_show.subscribe(self.hide)

        on_start.subscribe(self.start)

        on_exit.subscribe(self.exit)
        self.on_exit = on_exit

        self.icon = self.create_system_tray_icon()

    def create_system_tray_icon(self) -> icon:
        icon_image: Image = Image.open(ICON_PATH)

        menu: Tuple[MenuItem, MenuItem] = (
            MenuItem("Show Window", self.on_window_show.notify, default=True),
            MenuItem("Exit", self.on_exit.notify)
        )

        tray_icon: icon = Icon("20/20/20 Rule Notifier",
                               icon_image, "20/20/20 Notifier", menu)

        return tray_icon

    def start(self) -> None:
        self.icon.run_detached(lambda x: None)

    def hide(self) -> None:
        if self.icon.visible:
            self.icon.visible = False

    def show(self) -> None:
        if not self.icon.visible:
            self.icon.visible = True

    def exit(self) -> None:
        self.icon.visible = False
        self.icon.stop()
