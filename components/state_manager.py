from config.configuration import DURATIONS
from utils.event import Event
from utils.timer_status import TimerStatus


class StateManager:
    def __init__(self) -> None:
        self.on_status_change: Event = Event()

        self.status: TimerStatus = TimerStatus.WORKING

    def status_change(self) -> None:
        self.status = TimerStatus.BREAK if self.status == TimerStatus.WORKING else TimerStatus.WORKING
        self.on_status_change.notify(self._get_seconds())

    def status_reset(self) -> None:
        self.on_status_change.notify(self._get_seconds())

    def _get_seconds(self) -> int:
        return DURATIONS[self.status]
