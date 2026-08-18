from __future__ import annotations

import tkinter as tk

from ui.base_screen import BaseScreen
from ui.widgets import action_button, title_label


class SettingsScreen(BaseScreen):
    def __init__(self, parent: tk.Misc, controller: object) -> None:
        super().__init__(parent, controller)
        self.build()

    def build(self) -> None:
        title_label(self, "Settings", self.colours).pack(pady=(10, 6))
        body = tk.Frame(self, bg=self.colours["bg"]); body.pack(fill="both", expand=True, padx=22)
        self.theme_var = tk.StringVar(value=self.controller.state.settings.theme)
        self.round_var = tk.BooleanVar(value=self.controller.state.settings.round_safe_area)
        self.timeout_var = tk.IntVar(value=self.controller.state.settings.screen_timeout_seconds)
        tk.Label(body, text="Theme", bg=self.colours["bg"], fg=self.colours["fg"]).pack(anchor="w")
        tk.OptionMenu(body, self.theme_var, "Dark", "Light").pack(fill="x")
        tk.Checkbutton(body, text="Round display safe area", variable=self.round_var, bg=self.colours["bg"], fg=self.colours["fg"], selectcolor=self.colours["card"]).pack(anchor="w", pady=8)
        tk.Label(body, text="Screen timeout", bg=self.colours["bg"], fg=self.colours["fg"]).pack(anchor="w")
        tk.Scale(body, from_=5, to=120, orient="horizontal", variable=self.timeout_var, bg=self.colours["bg"], fg=self.colours["fg"], highlightthickness=0).pack(fill="x")
        buttons = tk.Frame(self, bg=self.colours["bg"]); buttons.pack(pady=8)
        action_button(buttons, "Save", self.save, self.colours).pack(side="left", padx=4)
        action_button(buttons, "Back", self.controller.go_back, self.colours).pack(side="left", padx=4)

    def on_show(self) -> None:
        settings = self.controller.state.settings
        self.theme_var.set(settings.theme); self.round_var.set(settings.round_safe_area); self.timeout_var.set(settings.screen_timeout_seconds)

    def save(self) -> None:
        settings = self.controller.state.settings
        settings.theme = self.theme_var.get(); settings.round_safe_area = self.round_var.get(); settings.screen_timeout_seconds = self.timeout_var.get(); settings.normalise()
        self.controller.save_state(); self.controller.refresh_all()
