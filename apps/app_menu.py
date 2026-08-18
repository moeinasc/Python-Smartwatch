from __future__ import annotations
import tkinter as tk
from ui.base_screen import BaseScreen
from ui.widgets import action_button, title_label

class AppsScreen(BaseScreen):
    APPS = [
        ("Health", "health", "HealthScreen"), ("Weather", "weather", "WeatherScreen"),
        ("Messages", "messages", "MessagesScreen"), ("Timer", "timer", "TimerScreen"),
        ("Stopwatch", "stopwatch", "StopwatchScreen"), ("Alarm", "alarm", "AlarmScreen"),
        ("Connectivity", "connectivity", "ConnectivityScreen"), ("Diagnostics", "diagnostics", "DiagnosticsScreen"),
        ("Settings", "settings", "SettingsScreen"), ("Notifications", "notifications", "NotificationsScreen"),
    ]
    def __init__(self, parent: tk.Misc, controller: object) -> None:
        super().__init__(parent, controller); self.build()

    def build(self) -> None:
        title_label(self, "Applications", self.colours).pack(pady=(8, 5))
        canvas = tk.Canvas(self, bg=self.colours["bg"], highlightthickness=0)
        canvas.pack(fill="both", expand=True, padx=8)
        grid = tk.Frame(canvas, bg=self.colours["bg"])
        canvas.create_window((0,0), window=grid, anchor="nw")
        for col in range(2): grid.grid_columnconfigure(col, weight=1, uniform="apps")
        for index, (label, icon_name, target) in enumerate(self.APPS):
            icon = self.controller.icons.get(icon_name, 32)
            button = tk.Button(grid, text=label, image=icon, compound="top", command=lambda name=target: self.controller.show_screen(name),
                bg=self.colours["card"], fg=self.colours["fg"], activebackground=self.colours["accent"], activeforeground=self.colours["bg"],
                relief="flat", bd=0, font=("Helvetica", 9, "bold"), padx=10, pady=6, cursor="hand2")
            button.image = icon
            button.grid(row=index//2, column=index%2, padx=4, pady=4, sticky="nsew")
        grid.update_idletasks(); canvas.configure(scrollregion=canvas.bbox("all"))
        action_button(self, "Home", self.controller.home, self.colours, font=("Helvetica", 9), pady=4).pack(pady=(2, 6))
