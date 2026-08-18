from __future__ import annotations

import time


class StopwatchModel:
    def __init__(self) -> None:
        self._started_at: float | None = None
        self._elapsed = 0.0

    @property
    def running(self) -> bool:
        return self._started_at is not None

    def start(self) -> None:
        if not self.running:
            self._started_at = time.monotonic()

    def pause(self) -> None:
        if self._started_at is not None:
            self._elapsed += time.monotonic() - self._started_at
            self._started_at = None

    def reset(self) -> None:
        self._started_at = None
        self._elapsed = 0.0

    def elapsed(self) -> float:
        if self._started_at is None:
            return self._elapsed
        return self._elapsed + time.monotonic() - self._started_at


class CountdownModel:
    def __init__(self, seconds: int = 60) -> None:
        self.duration = max(1, int(seconds))
        self._deadline: float | None = None
        self._remaining = float(self.duration)

    @property
    def running(self) -> bool:
        return self._deadline is not None

    def set_duration(self, seconds: int) -> None:
        self.duration = max(1, int(seconds))
        self.reset()

    def start(self) -> None:
        if not self.running and self._remaining > 0:
            self._deadline = time.monotonic() + self._remaining

    def pause(self) -> None:
        self._remaining = self.remaining()
        self._deadline = None

    def reset(self) -> None:
        self._deadline = None
        self._remaining = float(self.duration)

    def remaining(self) -> float:
        if self._deadline is None:
            return self._remaining
        return max(0.0, self._deadline - time.monotonic())
