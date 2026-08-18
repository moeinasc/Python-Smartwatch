from __future__ import annotations

import tkinter as tk
from tkinter import simpledialog
from datetime import datetime

from ui.base_screen import BaseScreen
from ui.widgets import action_button, title_label


class MessagesScreen(BaseScreen):
    def __init__(self, parent: tk.Misc, controller: object) -> None:
        super().__init__(parent, controller)
        self.build()

    def build(self) -> None:
        title_label(self, "Messages", self.colours).pack(pady=(10, 5))
        self.listbox = tk.Listbox(self, bg=self.colours["panel"], fg=self.colours["fg"], selectbackground=self.colours["accent"], relief="flat", font=("Helvetica", 10))
        self.listbox.pack(fill="both", expand=True, padx=16, pady=6)
        buttons = tk.Frame(self, bg=self.colours["bg"]); buttons.pack(pady=(0, 8))
        action_button(buttons, "New", self.new_message, self.colours, font=("Helvetica", 9), pady=5).pack(side="left", padx=3)
        action_button(buttons, "Back", self.controller.go_back, self.colours, font=("Helvetica", 9), pady=5).pack(side="left", padx=3)

    def on_show(self) -> None:
        self.listbox.delete(0, tk.END)
        messages = self.controller.state.messages
        if not messages:
            self.listbox.insert(tk.END, "No messages. Add a simulated message.")
        else:
            for item in reversed(messages):
                self.listbox.insert(tk.END, f"{item.get('time', '')}  {item.get('text', '')}")

    def new_message(self) -> None:
        text = simpledialog.askstring("Simulated message", "Message text:", parent=self)
        if text:
            self.controller.state.messages.append({"time": datetime.now().strftime("%H:%M"), "text": text[:120]})
            self.controller.notifications.add("New message", text[:80])
            self.controller.save_state()
            self.on_show()
