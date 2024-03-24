from typing import Any, Callable, List


class Event:
    def __init__(self) -> None:
        self.observers: List[Callable] = []

    def subscribe(self, observer: Callable) -> None:
        if observer not in self.observers:
            self.observers.append(observer)

    def unsubscribe(self, observer: Callable) -> None:
        if observer in self.observers:
            self.observers.remove(observer)

    def notify(self, *args, **kwargs) -> List[Any]:
        results: List[Any] = []

        for observer in self.observers:
            results.append(observer(*args, **kwargs))

        return results
