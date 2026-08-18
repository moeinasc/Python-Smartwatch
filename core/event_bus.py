from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from typing import Any


class EventBus:
    def __init__(self) -> None:
        self._subscribers: dict[str, list[Callable[..., None]]] = defaultdict(list)

    def subscribe(self, event: str, callback: Callable[..., None]) -> None:
        if callback not in self._subscribers[event]:
            self._subscribers[event].append(callback)

    def publish(self, event: str, **payload: Any) -> None:
        for callback in tuple(self._subscribers[event]):
            callback(**payload)
