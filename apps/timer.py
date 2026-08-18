from __future__ import annotations

import tkinter as tk

from core.scheduler import CountdownModel
from ui.base_screen import BaseScreen
from ui.widgets import action_button, format_duration, title_label


class TimerScreen(BaseScreen):
    def __init__(self, parent: tk.Misc, controller: object) -> None:
        self.model = CountdownModel(60)
        super().__init__(parent, controller)
        self.build()

    def build(self) -> None:
        title_label(self, "Timer", self.colours).pack(pady=(18, 12))
        self.display = tk.Label(self, text="01:00", bg=self.colours["bg"], fg=self.colours["accent"], font=("Helvetica", 40, "bold")); self.display.pack(pady=18)
        presets = tk.Frame(self, bg=self.colours["bg"]); presets.pack()
        for seconds, label in ((60, "1 min"), (300, "5 min"), (600, "10 min")):
            action_button(presets, label, lambda value=seconds: self._set(value), self.colours, font=("Helvetica", 9), pady=4).pack(side="left", padx=3)
        buttons = tk.Frame(self, bg=self.colours["bg"]); buttons.pack(pady=12)
        action_button(buttons, "Start/Pause", self.toggle, self.colours, font=("Helvetica", 9)).pack(side="left", padx=3)
        action_button(buttons, "Reset", self.reset, self.colours, font=("Helvetica", 9)).pack(side="left", padx=3)
        action_button(self, "Back", self.controller.go_back, self.colours, font=("Helvetica", 9), pady=4).pack()

    def _set(self, seconds: int) -> None:
        self.model.set_duration(seconds); self._update()

    def toggle(self) -> None:
        self.model.pause() if self.model.running else self.model.start(); self._update()

    def reset(self) -> None:
        self.model.reset(); self._update()

    def on_show(self) -> None:
        self._update()

    def _update(self) -> None:
        remaining = self.model.remaining(); self.display.configure(text=format_duration(remaining))
        if self.model.running and remaining <= 0:
            self.model.pause(); self.controller.notifications.add("Timer", "Timer completed")
            if self.controller.state.settings.vibration_enabled: self.controller.hardware.vibrate(500)
            self.controller.save_state()
        if self.model.running: self.schedule(200, self._update)
