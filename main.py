from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from core.config import load_config
from hardware.raspberry_pi import RaspberryPiHardware
from hardware.simulator import SimulatedHardware
from ui.controller import SmartwatchApp


def configure_logging() -> None:
    log_dir = Path.home() / ".python_smartwatch"
    log_dir.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(log_dir / "smartwatch.log", encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Python Smartwatch OS v3.1")
    parser.add_argument("--simulator", action="store_true", help="show desktop simulator controls")
    parser.add_argument("--fullscreen", action="store_true", help="start in full-screen mode")
    parser.add_argument(
        "--hardware",
        choices=("simulator", "raspberry-pi"),
        default="simulator",
        help="hardware adapter",
    )
    return parser.parse_args()


def main() -> int:
    configure_logging()
    args = parse_args()
    config = load_config()
    if args.fullscreen:
        config["display"]["fullscreen"] = True

    hardware = RaspberryPiHardware() if args.hardware == "raspberry-pi" else SimulatedHardware()
    app = SmartwatchApp(config=config, hardware=hardware, show_simulator=args.simulator)
    app.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
