from __future__ import annotations

import tkinter as tk

from ui.base_screen import BaseScreen
from ui.widgets import action_button, title_label


class HealthScreen(BaseScreen):
    def __init__(self, parent: tk.Misc, controller: object) -> None:
        super().__init__(parent, controller)
        self.build()

    def build(self) -> None:
        title_label(self, "Health", self.colours).pack(pady=(12, 8))
        self.hr = self._metric("Heart rate", "--")
        self.steps = self._metric("Steps", "--")
        self.temp = self._metric("Device sensor", "--")
        tk.Label(self, text="Prototype readings are informational only.", bg=self.colours["bg"], fg=self.colours["warning"], font=("Helvetica", 8)).pack(pady=8)
        nav = tk.Frame(self, bg=self.colours["bg"]); nav.pack()
        action_button(nav, "Refresh", self.on_show, self.colours).pack(side="left", padx=4)
        action_button(nav, "Back", self.controller.go_back, self.colours).pack(side="left", padx=4)

    def _metric(self, name: str, value: str) -> tk.Label:
        card = tk.Frame(self, bg=self.colours["card"])
        card.pack(fill="x", padx=30, pady=4)
        tk.Label(card, text=name, bg=self.colours["card"], fg=self.colours["muted"], font=("Helvetica", 9)).pack()
        label = tk.Label(card, text=value, bg=self.colours["card"], fg=self.colours["accent"], font=("Helvetica", 17, "bold"))
        label.pack(pady=(0, 5))
        return label

    def on_show(self) -> None:
        snap = self.controller.hardware.read_sensors()
        self.hr.configure(text="Unavailable" if snap.heart_rate_bpm is None else f"{snap.heart_rate_bpm} bpm")
        self.steps.configure(text=f"{snap.steps:,}")
        self.temp.configure(text="Unavailable" if snap.temperature_c is None else f"{snap.temperature_c:.1f} C")
