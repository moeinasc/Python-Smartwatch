import time
import unittest

from core.scheduler import CountdownModel, StopwatchModel


class SchedulerTests(unittest.TestCase):
    def test_stopwatch(self):
        model = StopwatchModel(); model.start(); time.sleep(0.01); model.pause()
        self.assertGreater(model.elapsed(), 0)
        model.reset(); self.assertEqual(model.elapsed(), 0)

    def test_countdown_configuration(self):
        model = CountdownModel(10)
        model.set_duration(30)
        self.assertEqual(int(model.remaining()), 30)


if __name__ == "__main__":
    unittest.main()
