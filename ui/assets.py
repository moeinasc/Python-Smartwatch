from __future__ import annotations
import tkinter as tk
from pathlib import Path

ASSET_DIR = Path(__file__).resolve().parents[1] / "assets" / "icons"

class IconManager:
    def __init__(self) -> None:
        self._cache: dict[tuple[str, int], tk.PhotoImage] = {}

    def get(self, name: str, size: int = 40) -> tk.PhotoImage | None:
        key = (name, size)
        if key in self._cache:
            return self._cache[key]
        path = ASSET_DIR / f"{name}.png"
        try:
            image = tk.PhotoImage(file=str(path))
            factor = max(1, round(96 / size))
            if factor > 1:
                image = image.subsample(factor, factor)
            self._cache[key] = image
            return image
        except tk.TclError:
            return None
