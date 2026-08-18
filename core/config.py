from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG_PATH = BASE_DIR / "config.json"

DEFAULT_CONFIG: dict[str, Any] = {
    "app_name": "Python Smartwatch",
    "version": "3.0.0",
    "display": {"width": 320, "height": 320, "round_safe_area": False, "fullscreen": False},
    "clock": {"use_24_hour": True},
    "power": {"screen_timeout_seconds": 30, "low_battery_threshold": 15},
    "simulation": {
        "weather_location": "Dresden",
        "weather_temperature_c": 21,
        "weather_condition": "Partly cloudy",
    },
}


def _merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    result = deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _merge(result[key], value)
        else:
            result[key] = value
    return result


def load_config(path: Path = DEFAULT_CONFIG_PATH) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return _merge(DEFAULT_CONFIG, json.load(handle))
    except (OSError, json.JSONDecodeError):
        return deepcopy(DEFAULT_CONFIG)
