from __future__ import annotations

import tkinter as tk

from ui.base_screen import BaseScreen
from ui.widgets import action_button, title_label


class QuickSettingsScreen(BaseScreen):
    def __init__(self, parent: tk.Misc, controller: object) -> None:
        super().__init__(parent, controller)
        self.build()

    def build(self) -> None:
        title_label(self, "Quick Settings", self.colours).pack(pady=(12, 8))
        self.grid_area = tk.Frame(self, bg=self.colours["bg"])
        self.grid_area.pack(fill="both", expand=True, padx=16)
        self.brightness = tk.Scale(self, from_=10, to=100, orient="horizontal", label="Brightness", command=self._brightness, bg=self.colours["bg"], fg=self.colours["fg"], highlightthickness=0)
        self.brightness.pack(fill="x", padx=28)
        action_button(self, "Back", self.controller.go_back, self.colours, font=("Helvetica", 9), pady=4).pack(pady=6)

    def on_show(self) -> None:
        for child in self.grid_area.winfo_children(): child.destroy()
        settings = self.controller.state.settings
        items = [("Wi-Fi", "wifi_enabled"), ("Bluetooth", "bluetooth_enabled"), ("Sound", "sound_enabled"), ("Vibration", "vibration_enabled"), ("Do not disturb", "do_not_disturb"), ("Power saver", "power_mode")]
        for index, (label, attribute) in enumerate(items):
            if attribute == "power_mode":
                enabled = settings.power_mode == "Battery saver"
            else:
                enabled = bool(getattr(settings, attribute))
            text = f"{label}\n{'ON' if enabled else 'OFF'}"
            action_button(self.grid_area, text, lambda attr=attribute: self._toggle(attr), self.colours, bg=self.colours["accent"] if enabled else self.colours["card"], fg=self.colours["bg"] if enabled else self.colours["fg"], font=("Helvetica", 9, "bold"), pady=6).grid(row=index//2, column=index%2, padx=4, pady=4, sticky="nsew")
            self.grid_area.grid_columnconfigure(index % 2, weight=1)
        self.brightness.set(settings.brightness)

    def _toggle(self, attribute: str) -> None:
        settings = self.controller.state.settings
        if attribute == "power_mode":
            settings.power_mode = "Normal" if settings.power_mode == "Battery saver" else "Battery saver"
        else:
            setattr(settings, attribute, not bool(getattr(settings, attribute)))
        self.controller.save_state(); self.on_show()

    def _brightness(self, value: str) -> None:
        self.controller.state.settings.brightness = int(float(value))
        self.controller.hardware.set_brightness(int(float(value)))
