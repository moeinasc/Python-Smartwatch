from __future__ import annotations

import logging
import platform

from hardware.interface import HardwareInterface, SensorSnapshot

LOGGER = logging.getLogger(__name__)


class RaspberryPiHardware(HardwareInterface):
    """Safe Raspberry Pi adapter scaffold.

    Replace the marked fallback methods with drivers for the exact I2C/SPI/GPIO
    components selected for the prototype. No GPIO library is imported here so
    the project can still be reviewed and tested away from the target board.
    """

    def __init__(self) -> None:
        self.brightness = 100
        self._fallback = SensorSnapshot(70, 0, 100, False, None, (0.0, 0.0, 1.0))

    def read_sensors(self) -> SensorSnapshot:
        # TODO: Read the selected heart-rate, motion, temperature and battery ICs.
        return self._fallback

    def vibrate(self, duration_ms: int) -> None:
        # TODO: Drive a vibration motor through a suitable transistor/driver.
        LOGGER.warning("Vibration requested for %d ms; no GPIO driver configured", duration_ms)

    def set_brightness(self, percent: int) -> None:
        self.brightness = max(10, min(100, int(percent)))
        # TODO: Connect this value to display backlight PWM where supported.

    def diagnostics(self) -> dict[str, str]:
        return {
            "Adapter": "Raspberry Pi scaffold",
            "Platform": platform.platform(),
            "Sensors": "Fallback values until drivers are configured",
            "Brightness": f"{self.brightness}%",
        }
