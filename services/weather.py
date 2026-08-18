from __future__ import annotations

from dataclasses import dataclass


@dataclass
class WeatherReading:
    location: str
    temperature_c: int
    condition: str
    source: str = "Simulated data"


class WeatherService:
    def __init__(self, config: dict) -> None:
        simulation = config.get("simulation", {})
        self._reading = WeatherReading(
            location=str(simulation.get("weather_location", "Dresden")),
            temperature_c=int(simulation.get("weather_temperature_c", 21)),
            condition=str(simulation.get("weather_condition", "Partly cloudy")),
        )

    def current(self) -> WeatherReading:
        return self._reading
