from __future__ import annotations

THEMES = {
    "Dark": {
        "bg": "#05070a",
        "panel": "#10151c",
        "card": "#18212b",
        "fg": "#f4f7fb",
        "muted": "#9ba8b8",
        "accent": "#35d7ff",
        "success": "#55e08a",
        "warning": "#ffcc45",
        "danger": "#ff5f6d",
    },
    "Light": {
        "bg": "#edf3f8",
        "panel": "#ffffff",
        "card": "#dfeaf2",
        "fg": "#102030",
        "muted": "#4f6173",
        "accent": "#0078a8",
        "success": "#168b4f",
        "warning": "#9a6800",
        "danger": "#bd2435",
    },
}


class ThemeManager:
    def __init__(self, name: str = "Dark") -> None:
        self.name = name if name in THEMES else "Dark"

    @property
    def colours(self) -> dict[str, str]:
        return THEMES[self.name]

    def set(self, name: str) -> None:
        self.name = name if name in THEMES else "Dark"
