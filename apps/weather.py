from __future__ import annotations

import tkinter as tk

from ui.base_screen import BaseScreen
from ui.widgets import action_button, title_label


class WeatherScreen(BaseScreen):
    def __init__(self, parent: tk.Misc, controller: object) -> None:
        super().__init__(parent, controller)
        self.build()

    def build(self) -> None:
        title_label(self, "Weather", self.colours).pack(pady=(20, 12))
        self.location = tk.Label(self, bg=self.colours["bg"], fg=self.colours["muted"], font=("Helvetica", 13))
        self.location.pack()
        self.temperature = tk.Label(self, bg=self.colours["bg"], fg=self.colours["accent"], font=("Helvetica", 42, "bold"))
        self.temperature.pack(pady=8)
        self.condition = tk.Label(self, bg=self.colours["bg"], fg=self.colours["fg"], font=("Helvetica", 14))
        self.condition.pack()
        self.source = tk.Label(self, bg=self.colours["bg"], fg=self.colours["warning"], font=("Helvetica", 8))
        self.source.pack(pady=12)
        action_button(self, "Back", self.controller.go_back, self.colours).pack()

    def on_show(self) -> None:
        weather = self.controller.weather.current()
        self.location.configure(text=weather.location)
        self.temperature.configure(text=f"{weather.temperature_c} C")
        self.condition.configure(text=weather.condition)
        self.source.configure(text=weather.source)
