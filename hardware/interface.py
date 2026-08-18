from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class SensorSnapshot:
    heart_rate_bpm: int | None
    steps: int
    battery_percent: int
    charging: bool
    temperature_c: float | None
    acceleration: tuple[float, float, float]


class HardwareInterface(ABC):
    @abstractmethod
    def read_sensors(self) -> SensorSnapshot:
        raise NotImplementedError

    @abstractmethod
    def vibrate(self, duration_ms: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def set_brightness(self, percent: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def diagnostics(self) -> dict[str, str]:
        raise NotImplementedError

    def close(self) -> None:
        return None
