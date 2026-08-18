import unittest

from hardware.simulator import SimulatedHardware


class HardwareTests(unittest.TestCase):
    def test_simulator_clamps_values(self):
        hardware = SimulatedHardware()
        hardware.update(battery_percent=200, heart_rate_bpm=500, steps=-1)
        snapshot = hardware.read_sensors()
        self.assertEqual(snapshot.battery_percent, 100)
        self.assertEqual(snapshot.heart_rate_bpm, 240)
        self.assertEqual(snapshot.steps, 0)

    def test_scenario(self):
        hardware = SimulatedHardware()
        hardware.apply_scenario("Low battery")
        self.assertEqual(hardware.read_sensors().battery_percent, 5)


if __name__ == "__main__":
    unittest.main()
