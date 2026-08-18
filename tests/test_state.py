import unittest

from core.state import WatchSettings, WatchState


class StateTests(unittest.TestCase):
    def test_settings_are_normalised(self):
        settings = WatchSettings(brightness=500, screen_timeout_seconds=1, theme="Unknown")
        settings.normalise()
        self.assertEqual(settings.brightness, 100)
        self.assertEqual(settings.screen_timeout_seconds, 5)
        self.assertEqual(settings.theme, "Dark")

    def test_state_round_trip(self):
        state = WatchState()
        state.notifications.append({"title": "Test", "body": "Hello"})
        restored = WatchState.from_dict(state.to_dict())
        self.assertEqual(restored.notifications[0]["title"], "Test")


if __name__ == "__main__":
    unittest.main()
