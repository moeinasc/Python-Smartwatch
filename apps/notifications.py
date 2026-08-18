from __future__ import annotations

import tkinter as tk

from ui.base_screen import BaseScreen
from ui.widgets import action_button, title_label


class NotificationsScreen(BaseScreen):
    def __init__(self, parent: tk.Misc, controller: object) -> None:
        super().__init__(parent, controller)
        self.build()

    def build(self) -> None:
        title_label(self, "Notifications", self.colours).pack(pady=(10, 5))
        self.listbox = tk.Listbox(self, bg=self.colours["panel"], fg=self.colours["fg"], selectbackground=self.colours["accent"], relief="flat", font=("Helvetica", 9))
        self.listbox.pack(fill="both", expand=True, padx=14, pady=6)
        buttons = tk.Frame(self, bg=self.colours["bg"]); buttons.pack(pady=(0, 8))
        action_button(buttons, "Read", self.mark_read, self.colours, font=("Helvetica", 8), pady=4).pack(side="left", padx=2)
        action_button(buttons, "Clear", self.clear, self.colours, font=("Helvetica", 8), pady=4).pack(side="left", padx=2)
        action_button(buttons, "Back", self.controller.go_back, self.colours, font=("Helvetica", 8), pady=4).pack(side="left", padx=2)

    def on_show(self) -> None:
        self.listbox.delete(0, tk.END)
        for note in reversed(self.controller.state.notifications):
            self.listbox.insert(tk.END, f"{note.get('time', '')}  {note.get('title', '')}: {note.get('body', '')}")
        if not self.controller.state.notifications:
            self.listbox.insert(tk.END, "No notifications")

    def mark_read(self) -> None:
        self.controller.notifications.mark_all_read(); self.controller.save_state(); self.on_show()

    def clear(self) -> None:
        self.controller.notifications.clear(); self.controller.save_state(); self.on_show()
