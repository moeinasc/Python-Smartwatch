from __future__ import annotations

import tkinter as tk
from datetime import datetime

from ui.base_screen import BaseScreen
from ui.widgets import action_button


class LockScreen(BaseScreen):
    def __init__(self, parent: tk.Misc, controller: object) -> None:
        super().__init__(parent, controller)
        self.build()

    def build(self) -> None:
        tk.Label(self, text="Python Smartwatch", bg=self.colours["bg"], fg=self.colours["accent"], font=("Helvetica", 11, "bold")).pack(pady=(28, 0))
        self.clock = tk.Label(self, bg=self.colours["bg"], fg=self.colours["fg"], font=("Helvetica", 42, "bold"))
        self.clock.pack(pady=(36, 4))
        self.date = tk.Label(self, bg=self.colours["bg"], fg=self.colours["muted"], font=("Helvetica", 12))
        self.date.pack()
        self.notice = tk.Label(self, bg=self.colours["bg"], fg=self.colours["warning"], font=("Helvetica", 10))
        self.notice.pack(pady=18)
        action_button(self, "Unlock", self.controller.unlock, self.colours, padx=30).pack()

    def on_show(self) -> None:
        self.controller.state.locked = True
        self._tick()

    def _tick(self) -> None:
        now = datetime.now()
        self.clock.configure(text=now.strftime("%H:%M"))
        self.date.configure(text=now.strftime("%a, %d %b"))
        unread = self.controller.state.unread_notifications
        self.notice.configure(text=f"{unread} unread notification{'s' if unread != 1 else ''}" if unread else "No new notifications")
        self.schedule(1000, self._tick)
