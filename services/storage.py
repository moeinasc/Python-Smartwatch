from __future__ import annotations

import json
import logging
from pathlib import Path

from core.state import WatchState

LOGGER = logging.getLogger(__name__)


class StateStore:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or Path.home() / ".python_smartwatch" / "state.json"

    def load(self) -> WatchState:
        try:
            with self.path.open("r", encoding="utf-8") as handle:
                return WatchState.from_dict(json.load(handle))
        except FileNotFoundError:
            return WatchState()
        except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
            LOGGER.warning("Could not load state from %s: %s", self.path, exc)
            return WatchState()

    def save(self, state: WatchState) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp = self.path.with_suffix(".tmp")
        with temp.open("w", encoding="utf-8") as handle:
            json.dump(state.to_dict(), handle, indent=2, ensure_ascii=False)
        temp.replace(self.path)
