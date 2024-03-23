from logging import warning
from threading import Thread
from time import sleep

from utils.event import Event


class Timer:
    def __init__(self, on_start: Event, on_exit: Event) -> None:
        on_start.subscribe(self.start)
        on_exit.subscribe(self.stop)

        self.on_change: Event = Event()
        self.on_end: Event = Event()

        self.time: int = 0
        self._timer: Thread = None

        self.active: bool = False

    def reset(self, seconds: int = 0) -> None:
        self.time = seconds
        self.stop()

        self.on_change.notify(self.time)

    def start(self) -> None:
        self._timer = Thread(target=lambda: self._reduce())

    def activate(self) -> None:
        self.active = True

        try:
            self._timer.start()
        except (RuntimeError):
            warning('Tried to start a running thread.')

    def stop(self) -> None:
        self.active = False

    def toggle(self, value: bool = None) -> None:
        if not value:
            value = not self.active

        if value:
            self.activate()
        else:
            self.stop()

    def _reduce(self) -> None:
        while self.time > 0 and self.active:
            self.time -= 1
            self.on_change.notify(self.time)

            sleep(1)

        if self.time == 0:
            self.on_end.notify()

        self._timer = Thread(target=lambda: self._reduce())
