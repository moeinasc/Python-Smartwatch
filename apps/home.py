from __future__ import annotations

import tkinter as tk
from datetime import datetime

from ui.base_screen import BaseScreen
from ui.widgets import action_button


class HomeScreen(BaseScreen):
    def __init__(self, parent: tk.Misc, controller: object) -> None:
        super().__init__(parent, controller)
        self.build()

    def build(self) -> None:
        margin = 28 if self.controller.state.settings.round_safe_area else 12
        self.top = tk.Frame(self, bg=self.colours["bg"])
        self.top.pack(fill="x", padx=margin, pady=(10, 0))
        self.status = tk.Label(self.top, bg=self.colours["bg"], fg=self.colours["muted"], font=("Helvetica", 9))
        self.status.pack(side="left")
        self.battery = tk.Label(self.top, bg=self.colours["bg"], fg=self.colours["success"], font=("Helvetica", 9, "bold"))
        self.battery.pack(side="right")
        self.time_label = tk.Label(self, bg=self.colours["bg"], fg=self.colours["fg"], font=("Helvetica", 39, "bold"))
        self.time_label.pack(pady=(32, 0))
        self.date_label = tk.Label(self, bg=self.colours["bg"], fg=self.colours["accent"], font=("Helvetica", 12))
        self.date_label.pack()
        self.health = tk.Label(self, bg=self.colours["bg"], fg=self.colours["muted"], font=("Helvetica", 11))
        self.health.pack(pady=18)
        buttons = tk.Frame(self, bg=self.colours["bg"])
        buttons.pack(fill="x", padx=margin)
        for label, icon_name, command in (("Apps", "apps", lambda: self.controller.show_screen("AppsScreen")), ("Quick", "quick", lambda: self.controller.show_screen("QuickSettingsScreen")), ("Lock", "lock", self.controller.lock)):
            icon = self.controller.icons.get(icon_name, 24)
            button = tk.Button(buttons, text=label, image=icon, compound="top", command=command, bg=self.colours["card"], fg=self.colours["fg"], activebackground=self.colours["accent"], activeforeground=self.colours["bg"], relief="flat", bd=0, font=("Helvetica", 8, "bold"), pady=5)
            button.image = icon
            button.pack(side="left", expand=True, fill="x", padx=3)
        self.controller.events.subscribe("long_press", self._long_press)

    def _long_press(self, screen: str | None = None) -> None:
        if screen == "HomeScreen":
            self.controller.show_screen("SettingsScreen")

    def on_show(self) -> None:
        self._tick()

    def _tick(self) -> None:
        now = datetime.now()
        use_24 = bool(self.controller.config_data.get("clock", {}).get("use_24_hour", True))
        self.time_label.configure(text=now.strftime("%H:%M") if use_24 else now.strftime("%I:%M %p").lstrip("0"))
        self.date_label.configure(text=now.strftime("%A, %d %B"))
        snap = self.controller.hardware.read_sensors()
        charge = " +" if snap.charging else ""
        self.battery.configure(text=f"BAT {snap.battery_percent}%{charge}", fg=self.colours["danger"] if snap.battery_percent <= 15 else self.colours["success"])
        self.status.configure(text=f"Wi-Fi {'ON' if self.controller.state.settings.wifi_enabled else 'OFF'}")
        hr = "Sensor unavailable" if snap.heart_rate_bpm is None else f"HR {snap.heart_rate_bpm} bpm"
        self.health.configure(text=f"{hr}   |   {snap.steps:,} steps")
        self.schedule(1000, self._tick)
