# Python Smartwatch OS v3.1

A modular Tkinter smartwatch simulator and Raspberry Pi-ready prototype.

## Included

- Animated branded splash screen and coherent SVG/PNG icon library
- Modern icon-card application launcher and watch-face controls
- Class-based screen controller with reusable screens
- Persistent JSON settings and state
- Desktop hardware simulator with controllable sensor values
- Hardware abstraction layer and Raspberry Pi adapter scaffold
- Clock, lock screen, app menu, alarm, timer, stopwatch and notifications
- Quick settings, health, weather, messages, connectivity and diagnostics
- Swipe navigation, long-press handling, keyboard/button mappings and screen timeout
- Square and round-display safe-area modes
- Logging, recovery screen and unit tests

## Requirements

- Python 3.10 or newer
- Tkinter
- Optional: `psutil` for richer diagnostics

On Debian/Raspberry Pi OS, Tkinter is commonly installed as `python3-tk`.

## Run

```bash
python main.py
```

Run with the simulator controls visible:

```bash
python main.py --simulator
```

Run full-screen:

```bash
python main.py --fullscreen
```

Select the Raspberry Pi adapter scaffold:

```bash
python main.py --hardware raspberry-pi --fullscreen
```

The Raspberry Pi adapter deliberately uses safe fallbacks until the methods in
`hardware/raspberry_pi.py` are connected to the exact display, sensors, GPIO,
battery monitor and vibration driver used by your prototype.

## Keyboard controls

- `Home`: home screen
- `Escape`: back, or exit full-screen mode
- `Left` / `Right`: previous/next main screen
- `Up` / `Down`: quick settings/notifications
- `Space`: simulated side button or wake
- `L`: lock
- `F11`: toggle full-screen

Mouse/touch gestures can also be used on the display:

- Swipe left/right: move between main screens
- Swipe down: quick settings
- Swipe up: notifications
- Long press: screen-specific action

## Configuration

The first run creates a writable state file in:

```text
~/.python_smartwatch/state.json
```

Edit `config.json` to choose resolution, round safe area, time format and screen
timeout defaults.

## Tests

```bash
python -m unittest discover -s tests -v
```

## Project layout

- `core/`: controller-independent state, scheduler, events and power logic
- `ui/`: screen classes, theme and reusable widgets
- `apps/`: watch applications
- `hardware/`: simulator and Raspberry Pi abstraction
- `services/`: persistence, connectivity, notifications and weather simulation
- `tests/`: state, timer and hardware tests

## Hardware migration path

1. Validate the complete interface on desktop with `--simulator`.
2. Run the same software on Raspberry Pi OS with a small touchscreen.
3. Implement the functions marked `TODO` in `hardware/raspberry_pi.py` for the
   selected GPIO and sensor hardware.
4. For a low-power microcontroller version, retain the state/service concepts
   but replace the Tkinter presentation layer with LVGL/MicroPython.

## Icon assets

The `assets/icons` directory contains editable SVG masters and 96 px PNG runtime versions. The icon manager caches images and safely falls back to text when an asset cannot be loaded.
