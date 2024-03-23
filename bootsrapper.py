from components.notifier import Notifier
from components.state_manager import StateManager
from components.window import Window
from components.tray_icon import TrayIcon
from config.configuration import SHOULD_SHOW_WINDOW_ON_TIMER_END, SHOULD_START_ON_STARTUP
from utils.event import Event
from components.timer import Timer


class Bootsrapper:
    def __init__(self) -> None:
        self.on_start: Event = Event()
        self.on_exit: Event = Event()

        self.tray_icon: TrayIcon = TrayIcon(self.on_start, self.on_exit)
        self.timer: Timer = Timer(self.on_start, self.on_exit)
        self.state_manager: StateManager = StateManager()
        self.notifier: Notifier = Notifier(self.on_start, self.on_exit)
        self.window: Window = Window(
            self.on_start, self.on_exit, self.timer.on_end)

        self.bind_events()

    def bind_events(self) -> None:
        self.window.on_window_hide.subscribe(self.tray_icon.show)
        self.tray_icon.on_window_show.subscribe(self.window.show_window)

        self.window.on_change_time.subscribe(self.timer.reset)
        self.window.on_change_timer_status.subscribe(self.timer.toggle)
        self.timer.on_change.subscribe(self.window.timer_change)

        self.timer.on_end.subscribe(self.state_manager.status_change)
        self.timer.on_end.subscribe(self.notifier.play_sound)
        self.state_manager.on_status_change.subscribe(self.timer.reset)

        self.window.on_reset.subscribe(self.state_manager.status_reset)

        if SHOULD_SHOW_WINDOW_ON_TIMER_END:
            self.timer.on_end.subscribe(self.tray_icon.on_window_show.notify)

    def bootstrap(self) -> None:
        if SHOULD_START_ON_STARTUP:
            self.window.root.after_idle(
                self.window.on_change_timer_status.notify)

        self.on_start.notify()
