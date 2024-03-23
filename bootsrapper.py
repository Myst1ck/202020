from components.window import Window
from components.tray_icon import TrayIcon
from utils.event import Event
from components.timer import Timer


class Bootsrapper:
    def __init__(self) -> None:
        self.on_start: Event = Event()
        self.on_exit: Event = Event()

        self.tray_icon: TrayIcon = TrayIcon(self.on_start, self.on_exit)
        self.timer: Timer = Timer(self.on_start, self.on_exit)
        self.window: Window = Window(self.on_start, self.on_exit)

        self.bind_events()

    def bind_events(self) -> None:
        self.window.on_window_hide.subscribe(self.tray_icon.show)
        self.tray_icon.on_window_show.subscribe(self.window.show_window)

        self.window.on_change_time.subscribe(self.timer.reset)
        self.window.on_change_timer_status.subscribe(self.timer.toggle)
        self.timer.on_change.subscribe(self.window.timer_change)

    def bootstrap(self) -> None:
        self.on_start.notify()
