from __future__ import annotations

import tkinter as tk
from datetime import datetime

from ui.base_screen import BaseScreen
from ui.widgets import action_button, title_label


class AlarmScreen(BaseScreen):
    def __init__(self, parent: tk.Misc, controller: object) -> None:
        self.enabled = False
        super().__init__(parent, controller); self.build()

    def build(self) -> None:
        title_label(self, "Alarm", self.colours).pack(pady=(20, 12))
        self.hour = tk.Spinbox(self, from_=0, to=23, width=4, font=("Helvetica", 18), format="%02.0f")
        self.hour.pack(side="left", padx=(80, 2), pady=35)
        self.minute = tk.Spinbox(self, from_=0, to=59, width=4, font=("Helvetica", 18), format="%02.0f")
        self.minute.pack(side="left", padx=2, pady=35)
        self.status = tk.Label(self, text="Alarm off", bg=self.colours["bg"], fg=self.colours["muted"], font=("Helvetica", 11)); self.status.place(relx=.5, rely=.62, anchor="center")
        buttons = tk.Frame(self, bg=self.colours["bg"]); buttons.place(relx=.5, rely=.78, anchor="center")
        action_button(buttons, "Toggle", self.toggle, self.colours).pack(side="left", padx=4)
        action_button(buttons, "Back", self.controller.go_back, self.colours).pack(side="left", padx=4)

    def toggle(self) -> None:
        self.enabled = not self.enabled
        value = f"{int(self.hour.get()):02d}:{int(self.minute.get()):02d}"
        self.status.configure(text=f"Alarm {value}" if self.enabled else "Alarm off", fg=self.colours["success"] if self.enabled else self.colours["muted"])
        if self.enabled: self._check()

    def _check(self) -> None:
        if not self.enabled: return
        now = datetime.now().strftime("%H:%M")
        target = f"{int(self.hour.get()):02d}:{int(self.minute.get()):02d}"
        if now == target:
            self.enabled = False; self.controller.notifications.add("Alarm", f"Alarm at {target}")
            if self.controller.state.settings.vibration_enabled: self.controller.hardware.vibrate(1000)
            self.controller.save_state(); self.status.configure(text="Alarm complete")
        else: self.schedule(1000, self._check)
