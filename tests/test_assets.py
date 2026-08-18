import unittest
from pathlib import Path

class AssetTests(unittest.TestCase):
    def test_required_icons_exist(self):
        root = Path(__file__).resolve().parents[1] / "assets" / "icons"
        for name in ("logo", "apps", "health", "weather", "messages", "settings", "notifications"):
            self.assertTrue((root / f"{name}.svg").exists())
            self.assertTrue((root / f"{name}.png").exists())

if __name__ == "__main__": unittest.main()
