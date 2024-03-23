from threading import Thread
from typing import Callable, List


class Event:
    def __init__(self) -> None:
        self.observers: List[Callable] = []

    def subscribe(self, observer: Callable) -> None:
        self.observers.append(observer)

    def unsubscribe(self, observer: Callable) -> None:
        self.observers.remove(observer)

    def notify(self, *args, **kwargs) -> None:
        for observer in self.observers:
            observer(*args, **kwargs)
