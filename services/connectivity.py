from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ConnectivityService:
    wifi_enabled: bool = True
    bluetooth_enabled: bool = True
    mobile_data_enabled: bool = False

    @property
    def wifi_status(self) -> str:
        return "Connected (simulated)" if self.wifi_enabled else "Off"

    @property
    def bluetooth_status(self) -> str:
        return "Connected (simulated)" if self.bluetooth_enabled else "Off"

    def sync_from_settings(self, settings: object) -> None:
        self.wifi_enabled = bool(getattr(settings, "wifi_enabled", False))
        self.bluetooth_enabled = bool(getattr(settings, "bluetooth_enabled", False))
        self.mobile_data_enabled = bool(getattr(settings, "mobile_data_enabled", False))
