from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class WatchSettings:
    brightness: int = 100
    bluetooth_enabled: bool = True
    wifi_enabled: bool = True
    mobile_data_enabled: bool = False
    power_mode: str = "Normal"
    sound_enabled: bool = True
    vibration_enabled: bool = True
    theme: str = "Dark"
    do_not_disturb: bool = False
    screen_timeout_seconds: int = 30
    round_safe_area: bool = False

    def normalise(self) -> None:
        self.brightness = max(10, min(100, int(self.brightness)))
        self.screen_timeout_seconds = max(5, min(300, int(self.screen_timeout_seconds)))
        if self.power_mode not in {"Normal", "Battery saver", "Performance"}:
            self.power_mode = "Normal"
        if self.theme not in {"Dark", "Light"}:
            self.theme = "Dark"


@dataclass
class WatchState:
    settings: WatchSettings = field(default_factory=WatchSettings)
    locked: bool = False
    notifications: list[dict[str, Any]] = field(default_factory=list)
    unread_notifications: int = 0
    messages: list[dict[str, str]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "WatchState":
        raw_settings = data.get("settings", {})
        permitted = WatchSettings.__dataclass_fields__.keys()
        settings = WatchSettings(**{k: v for k, v in raw_settings.items() if k in permitted})
        settings.normalise()
        return cls(
            settings=settings,
            locked=bool(data.get("locked", False)),
            notifications=list(data.get("notifications", []))[-50:],
            unread_notifications=max(0, int(data.get("unread_notifications", 0))),
            messages=list(data.get("messages", []))[-50:],
        )
