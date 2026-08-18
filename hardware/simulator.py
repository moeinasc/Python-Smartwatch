from __future__ import annotations

import logging
from dataclasses import replace

from hardware.interface import HardwareInterface, SensorSnapshot

LOGGER = logging.getLogger(__name__)


class SimulatedHardware(HardwareInterface):
    def __init__(self) -> None:
        self._snapshot = SensorSnapshot(
            heart_rate_bpm=72,
            steps=3456,
            battery_percent=84,
            charging=False,
            temperature_c=24.0,
            acceleration=(0.0, 0.0, 1.0),
        )
        self.brightness = 100
        self.last_vibration_ms = 0

    def read_sensors(self) -> SensorSnapshot:
        return self._snapshot

    def update(self, **values: object) -> None:
        allowed = SensorSnapshot.__dataclass_fields__.keys()
        clean = {key: value for key, value in values.items() if key in allowed}
        if "battery_percent" in clean:
            clean["battery_percent"] = max(0, min(100, int(clean["battery_percent"])))
        if "heart_rate_bpm" in clean and clean["heart_rate_bpm"] is not None:
            clean["heart_rate_bpm"] = max(30, min(240, int(clean["heart_rate_bpm"])))
        if "steps" in clean:
            clean["steps"] = max(0, int(clean["steps"]))
        self._snapshot = replace(self._snapshot, **clean)

    def apply_scenario(self, name: str) -> None:
        scenarios = {
            "Normal": dict(heart_rate_bpm=72, steps=3456, battery_percent=84, charging=False),
            "Low battery": dict(heart_rate_bpm=70, steps=6789, battery_percent=5, charging=False),
            "Charging": dict(heart_rate_bpm=68, steps=2222, battery_percent=61, charging=True),
            "Sensor failure": dict(heart_rate_bpm=None, temperature_c=None, battery_percent=52),
        }
        self.update(**scenarios.get(name, scenarios["Normal"]))

    def vibrate(self, duration_ms: int) -> None:
        self.last_vibration_ms = max(0, int(duration_ms))
        LOGGER.info("Simulated vibration: %d ms", self.last_vibration_ms)

    def set_brightness(self, percent: int) -> None:
        self.brightness = max(10, min(100, int(percent)))

    def diagnostics(self) -> dict[str, str]:
        return {
            "Adapter": "Desktop simulator",
            "Sensors": "Simulated",
            "Brightness": f"{self.brightness}%",
            "Last vibration": f"{self.last_vibration_ms} ms",
        }
