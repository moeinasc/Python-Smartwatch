from __future__ import annotations

import tkinter as tk

from ui.base_screen import BaseScreen
from ui.widgets import action_button, title_label


class ConnectivityScreen(BaseScreen):
    def __init__(self, parent: tk.Misc, controller: object) -> None:
        super().__init__(parent, controller); self.build()

    def build(self) -> None:
        title_label(self, "Connectivity", self.colours).pack(pady=(18, 14))
        self.wifi = self._row("Wi-Fi")
        self.bluetooth = self._row("Bluetooth")
        self.mobile = self._row("Mobile data")
        tk.Label(self, text="Connectivity services are simulated in v3.0.", bg=self.colours["bg"], fg=self.colours["warning"], font=("Helvetica", 8)).pack(pady=12)
        action_button(self, "Back", self.controller.go_back, self.colours).pack()

    def _row(self, label: str) -> tk.Label:
        frame = tk.Frame(self, bg=self.colours["card"]); frame.pack(fill="x", padx=32, pady=5)
        tk.Label(frame, text=label, bg=self.colours["card"], fg=self.colours["muted"]).pack(side="left", padx=8, pady=8)
        value = tk.Label(frame, bg=self.colours["card"], fg=self.colours["success"], font=("Helvetica", 9, "bold")); value.pack(side="right", padx=8)
        return value

    def on_show(self) -> None:
        self.controller.connectivity.sync_from_settings(self.controller.state.settings)
        self.wifi.configure(text=self.controller.connectivity.wifi_status)
        self.bluetooth.configure(text=self.controller.connectivity.bluetooth_status)
        self.mobile.configure(text="On" if self.controller.connectivity.mobile_data_enabled else "Off")
