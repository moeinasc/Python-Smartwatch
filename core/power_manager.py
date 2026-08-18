from __future__ import annotations

import time


class PowerManager:
    def __init__(self, timeout_seconds: int = 30) -> None:
        self.timeout_seconds = max(5, timeout_seconds)
        self.last_activity = time.monotonic()
        self.screen_awake = True

    def activity(self) -> None:
        self.last_activity = time.monotonic()
        self.screen_awake = True

    def should_sleep(self) -> bool:
        return self.screen_awake and time.monotonic() - self.last_activity >= self.timeout_seconds

    def sleep(self) -> None:
        self.screen_awake = False

    def wake(self) -> None:
        self.activity()
