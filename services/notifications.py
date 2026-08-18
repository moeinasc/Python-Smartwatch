from __future__ import annotations

from datetime import datetime

from core.state import WatchState


class NotificationService:
    def __init__(self, state: WatchState) -> None:
        self.state = state

    def add(self, title: str, body: str) -> None:
        self.state.notifications.append(
            {"title": title, "body": body, "time": datetime.now().strftime("%H:%M")}
        )
        self.state.notifications = self.state.notifications[-50:]
        self.state.unread_notifications += 1

    def mark_all_read(self) -> None:
        self.state.unread_notifications = 0

    def clear(self) -> None:
        self.state.notifications.clear()
        self.state.unread_notifications = 0
