from __future__ import annotations

import tkinter as tk

from core.scheduler import StopwatchModel
from ui.base_screen import BaseScreen
from ui.widgets import action_button, format_duration, title_label


class StopwatchScreen(BaseScreen):
    def __init__(self, parent: tk.Misc, controller: object) -> None:
        self.model = StopwatchModel()
        super().__init__(parent, controller); self.build()

    def build(self) -> None:
        title_label(self, "Stopwatch", self.colours).pack(pady=(24, 12))
        self.display = tk.Label(self, text="00:00", bg=self.colours["bg"], fg=self.colours["accent"], font=("Helvetica", 38, "bold")); self.display.pack(pady=25)
        buttons = tk.Frame(self, bg=self.colours["bg"]); buttons.pack()
        action_button(buttons, "Start/Pause", self.toggle, self.colours).pack(side="left", padx=4)
        action_button(buttons, "Reset", self.reset, self.colours).pack(side="left", padx=4)
        action_button(self, "Back", self.controller.go_back, self.colours, font=("Helvetica", 9), pady=4).pack(pady=15)

    def toggle(self) -> None:
        self.model.pause() if self.model.running else self.model.start(); self._update()

    def reset(self) -> None:
        self.model.reset(); self._update()

    def on_show(self) -> None: self._update()

    def _update(self) -> None:
        self.display.configure(text=format_duration(self.model.elapsed()))
        if self.model.running: self.schedule(100, self._update)
