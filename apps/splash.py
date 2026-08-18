from __future__ import annotations
import tkinter as tk
from ui.base_screen import BaseScreen

class SplashScreen(BaseScreen):
    def __init__(self, parent: tk.Misc, controller: object) -> None:
        super().__init__(parent, controller)
        self._progress = 0
        self.build()

    def build(self) -> None:
        body = tk.Frame(self, bg=self.colours["bg"])
        body.place(relx=.5, rely=.48, anchor="center")
        logo = self.controller.icons.get("logo", 72)
        self.logo_label = tk.Label(body, image=logo, bg=self.colours["bg"])
        self.logo_label.image = logo
        self.logo_label.pack(pady=(0, 8))
        tk.Label(body, text="PYTHON SMARTWATCH", bg=self.colours["bg"], fg=self.colours["fg"], font=("Helvetica", 16, "bold")).pack()
        tk.Label(body, text="OS 3.1", bg=self.colours["bg"], fg=self.colours["accent"], font=("Helvetica", 10, "bold")).pack(pady=(3, 18))
        self.canvas = tk.Canvas(body, width=180, height=6, bg=self.colours["panel"], highlightthickness=0)
        self.canvas.pack()
        self.bar = self.canvas.create_rectangle(0, 0, 0, 6, fill=self.colours["accent"], outline="")
        self.status = tk.Label(body, text="Starting services", bg=self.colours["bg"], fg=self.colours["muted"], font=("Helvetica", 8))
        self.status.pack(pady=7)

    def on_show(self) -> None:
        self._progress = 0
        self._animate()

    def _animate(self) -> None:
        self._progress = min(100, self._progress + 4)
        self.canvas.coords(self.bar, 0, 0, self._progress * 1.8, 6)
        if self._progress < 35: self.status.configure(text="Starting services")
        elif self._progress < 70: self.status.configure(text="Loading applications")
        else: self.status.configure(text="Preparing watch face")
        if self._progress >= 100:
            self.schedule(220, self.controller.finish_boot)
        else:
            self.schedule(35, self._animate)
