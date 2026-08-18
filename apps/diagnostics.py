from __future__ import annotations

import os
import platform
import tkinter as tk
from pathlib import Path

from ui.base_screen import BaseScreen
from ui.widgets import action_button, title_label

try:
    import psutil
except ImportError:
    psutil = None


class DiagnosticsScreen(BaseScreen):
    def __init__(self, parent: tk.Misc, controller: object) -> None:
        super().__init__(parent, controller); self.build()

    def build(self) -> None:
        title_label(self, "Diagnostics", self.colours).pack(pady=(8, 4))
        self.text = tk.Text(self, bg=self.colours["panel"], fg=self.colours["fg"], relief="flat", font=("Courier", 8), wrap="word", height=18)
        self.text.pack(fill="both", expand=True, padx=12, pady=4)
        buttons = tk.Frame(self, bg=self.colours["bg"]); buttons.pack(pady=6)
        action_button(buttons, "Refresh", self.on_show, self.colours, font=("Helvetica", 8), pady=4).pack(side="left", padx=3)
        action_button(buttons, "Self-test", self.self_test, self.colours, font=("Helvetica", 8), pady=4).pack(side="left", padx=3)
        action_button(buttons, "Back", self.controller.go_back, self.colours, font=("Helvetica", 8), pady=4).pack(side="left", padx=3)

    def on_show(self) -> None:
        info = {
            "Version": self.controller.config_data.get("version", "3.0.0"),
            "Python": platform.python_version(),
            "Platform": platform.platform(),
            "PID": str(os.getpid()),
            "State file": str(self.controller.store.path),
            "Log file": str(Path.home() / ".python_smartwatch" / "smartwatch.log"),
        }
        if psutil:
            info["CPU"] = f"{psutil.cpu_percent(interval=None)}%"
            info["Memory"] = f"{psutil.virtual_memory().percent}%"
        else:
            info["System metrics"] = "Install optional psutil"
        info.update(self.controller.hardware.diagnostics())
        self.text.configure(state="normal"); self.text.delete("1.0", tk.END)
        self.text.insert("1.0", "\n".join(f"{key}: {value}" for key, value in info.items())); self.text.configure(state="disabled")

    def self_test(self) -> None:
        snap = self.controller.hardware.read_sensors()
        checks = [
            ("Battery", 0 <= snap.battery_percent <= 100),
            ("Steps", snap.steps >= 0),
            ("State storage", self._storage_test()),
        ]
        self.controller.hardware.vibrate(100)
        result = "\n".join(f"{name}: {'PASS' if passed else 'FAIL'}" for name, passed in checks)
        self.text.configure(state="normal"); self.text.delete("1.0", tk.END); self.text.insert("1.0", result); self.text.configure(state="disabled")

    def _storage_test(self) -> bool:
        try:
            self.controller.save_state(); return self.controller.store.path.exists()
        except OSError:
            return False
