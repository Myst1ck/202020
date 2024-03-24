from components.notifier import Notifier
from components.settings_window import SettingsWindow
from components.state_manager import StateManager
from components.notifier_window import NotifierWindow
from components.tray_icon import TrayIcon
from utils.event import Event
from components.timer import Timer
from utils.settings_reader import SettingsReader


class Bootsrapper:
    def __init__(self) -> None:
        self.on_start: Event = Event()
        self.on_exit: Event = Event()

        self.settings_reader: SettingsReader = SettingsReader()

        self.tray_icon: TrayIcon = TrayIcon(self.on_start, self.on_exit)
        self.timer: Timer = Timer(self.on_start, self.on_exit)
        self.state_manager: StateManager = StateManager(self.settings_reader)
        self.notifier: Notifier = Notifier(self.on_start, self.on_exit)

        self.settings_window: SettingsWindow = SettingsWindow(
            self.on_exit, self.settings_reader)
        self.window: NotifierWindow = NotifierWindow(
            self.on_start, self.on_exit, self.timer.on_end, self.settings_reader)

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

        self.timer.on_end.subscribe(
            lambda: self.window.change_state_button('Continue'))
        self.window.on_reset.subscribe(
            lambda: self.window.change_state_button('Continue'))

        self.window.on_settings_show.subscribe(self.settings_window.start)

        if self.settings_reader.get_value('SHOULD_SHOW_WINDOW_ON_TIMER_END'):
            self.timer.on_end.subscribe(self.tray_icon.on_window_show.notify)

        self.settings_window.on_settings_change.subscribe(
            self.settings_changed)
        self.settings_window.on_settings_change.subscribe(
            self.window.change_closing_protocol)

    def bootstrap(self) -> None:
        if self.settings_reader.get_value('SHOULD_START_ON_STARTUP'):
            self.window.root.after_idle(
                self.window.on_change_timer_status.notify)

        self.on_start.notify()

    def settings_changed(self) -> None:
        if self.settings_reader.get_value('SHOULD_SHOW_WINDOW_ON_TIMER_END'):
            self.timer.on_end.subscribe(self.tray_icon.on_window_show.notify)
        else:
            self.timer.on_end.unsubscribe(self.tray_icon.on_window_show.notify)
