from __future__ import annotations

import tkinter as tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui.controller import SmartwatchApp


class BaseScreen(tk.Frame):
    def __init__(self, parent: tk.Misc, controller: "SmartwatchApp") -> None:
        self.controller = controller
        self.colours = controller.theme.colours
        super().__init__(parent, bg=self.colours["bg"])
        self._after_ids: set[str] = set()

    def on_show(self) -> None:
        return None

    def on_hide(self) -> None:
        for after_id in tuple(self._after_ids):
            try:
                self.after_cancel(after_id)
            except tk.TclError:
                pass
        self._after_ids.clear()

    def schedule(self, milliseconds: int, callback: object) -> None:
        holder: dict[str, str] = {}

        def run() -> None:
            after_id = holder.get("id")
            if after_id:
                self._after_ids.discard(after_id)
            callback()  # type: ignore[operator]

        holder["id"] = self.after(milliseconds, run)
        self._after_ids.add(holder["id"])

    def rebuild(self) -> None:
        for child in self.winfo_children():
            child.destroy()
        self.colours = self.controller.theme.colours
        self.configure(bg=self.colours["bg"])
        self.build()

    def build(self) -> None:
        raise NotImplementedError

    def back_button(self) -> tk.Button:
        from ui.widgets import action_button
        return action_button(self, "Back", self.controller.go_back, self.colours, font=("Helvetica", 9, "bold"), pady=4)
