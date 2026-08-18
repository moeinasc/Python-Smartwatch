from __future__ import annotations

import tkinter as tk
from collections.abc import Callable


def action_button(parent: tk.Misc, text: str, command: Callable[[], None], colours: dict[str, str], **kwargs: object) -> tk.Button:
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=kwargs.pop("bg", colours["card"]),
        fg=kwargs.pop("fg", colours["fg"]),
        activebackground=colours["accent"],
        activeforeground=colours["bg"],
        relief="flat",
        bd=0,
        cursor="hand2",
        font=kwargs.pop("font", ("Helvetica", 11, "bold")),
        padx=kwargs.pop("padx", 10),
        pady=kwargs.pop("pady", 8),
        **kwargs,
    )


def title_label(parent: tk.Misc, text: str, colours: dict[str, str]) -> tk.Label:
    return tk.Label(parent, text=text, bg=colours["bg"], fg=colours["fg"], font=("Helvetica", 17, "bold"))


def format_duration(seconds: float) -> str:
    total = max(0, int(seconds))
    minutes, sec = divmod(total, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{sec:02d}" if hours else f"{minutes:02d}:{sec:02d}"
