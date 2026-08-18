from __future__ import annotations

import logging
import tkinter as tk
from tkinter import messagebox

from apps.alarm import AlarmScreen
from apps.app_menu import AppsScreen
from apps.connectivity import ConnectivityScreen
from apps.diagnostics import DiagnosticsScreen
from apps.health import HealthScreen
from apps.home import HomeScreen
from apps.lock_screen import LockScreen
from apps.messages import MessagesScreen
from apps.notifications import NotificationsScreen
from apps.quick_settings import QuickSettingsScreen
from apps.settings import SettingsScreen
from apps.splash import SplashScreen
from apps.stopwatch import StopwatchScreen
from apps.timer import TimerScreen
from apps.weather import WeatherScreen
from core.event_bus import EventBus
from core.power_manager import PowerManager
from hardware.interface import HardwareInterface
from hardware.simulator import SimulatedHardware
from services.connectivity import ConnectivityService
from services.notifications import NotificationService
from services.storage import StateStore
from services.weather import WeatherService
from ui.theme import ThemeManager
from ui.assets import IconManager

LOGGER = logging.getLogger(__name__)


class SmartwatchApp(tk.Tk):
    MAIN_SCREENS = ["HomeScreen", "AppsScreen", "HealthScreen", "WeatherScreen"]

    def __init__(self, config: dict, hardware: HardwareInterface, show_simulator: bool = False) -> None:
        super().__init__()
        self.config_data = config
        self.hardware = hardware
        self.store = StateStore()
        self.state = self.store.load()
        self._apply_config_defaults()
        self.theme = ThemeManager(self.state.settings.theme)
        self.icons = IconManager()
        self.events = EventBus()
        self.notifications = NotificationService(self.state)
        self.connectivity = ConnectivityService()
        self.connectivity.sync_from_settings(self.state.settings)
        self.weather = WeatherService(config)
        self.power = PowerManager(self.state.settings.screen_timeout_seconds)
        self.screens: dict[str, tk.Frame] = {}
        self.current_screen: str | None = None
        self.history: list[str] = []
        self.fullscreen = bool(config["display"].get("fullscreen", False))
        self._touch_start: tuple[int, int, int] | None = None
        self._long_press_id: str | None = None
        self._simulator_panel: tk.Frame | None = None

        width = int(config["display"].get("width", 320))
        height = int(config["display"].get("height", 320))
        panel_width = 260 if show_simulator and isinstance(hardware, SimulatedHardware) else 0
        self.title(f"{config.get('app_name', 'Python Smartwatch')} v{config.get('version', '3.0.0')}")
        self.geometry(f"{width + panel_width}x{height}")
        self.minsize(width, height)
        self.configure(bg=self.theme.colours["bg"])
        self.attributes("-fullscreen", self.fullscreen)

        outer = tk.Frame(self, bg=self.theme.colours["bg"])
        outer.pack(fill="both", expand=True)
        outer.grid_rowconfigure(0, weight=1)
        outer.grid_columnconfigure(1 if panel_width else 0, weight=1)

        if panel_width:
            self._simulator_panel = tk.Frame(outer, width=panel_width, bg="#20262e")
            self._simulator_panel.grid(row=0, column=0, sticky="nsew")
            self._simulator_panel.grid_propagate(False)
            self._build_simulator_panel(self._simulator_panel)

        self.screen_container = tk.Frame(outer, bg=self.theme.colours["bg"], width=width, height=height)
        self.screen_container.grid(row=0, column=1 if panel_width else 0, sticky="nsew")
        self.screen_container.grid_propagate(False)
        self.screen_container.grid_rowconfigure(0, weight=1)
        self.screen_container.grid_columnconfigure(0, weight=1)

        self._create_screens()
        self._bind_controls()
        self.protocol("WM_DELETE_WINDOW", self.shutdown)
        self.show_screen("SplashScreen", add_history=False)
        self.after(1000, self._power_tick)

    def _apply_config_defaults(self) -> None:
        power = self.config_data.get("power", {})
        display = self.config_data.get("display", {})
        self.state.settings.screen_timeout_seconds = int(
            self.state.settings.screen_timeout_seconds or power.get("screen_timeout_seconds", 30)
        )
        self.state.settings.round_safe_area = bool(
            self.state.settings.round_safe_area or display.get("round_safe_area", False)
        )
        self.state.settings.normalise()

    def _create_screens(self) -> None:
        classes = (
            SplashScreen, HomeScreen, LockScreen, AppsScreen, QuickSettingsScreen,
            NotificationsScreen, HealthScreen, WeatherScreen, MessagesScreen,
            SettingsScreen, TimerScreen, StopwatchScreen, AlarmScreen,
            ConnectivityScreen, DiagnosticsScreen,
        )
        for screen_class in classes:
            screen = screen_class(self.screen_container, self)
            screen.grid(row=0, column=0, sticky="nsew")
            self.screens[screen_class.__name__] = screen

    def show_screen(self, name: str, add_history: bool = True) -> None:
        try:
            if name not in self.screens:
                raise KeyError(f"Unknown screen: {name}")
            if self.current_screen == name:
                self.screens[name].event_generate("<<Refresh>>")
                return
            if self.current_screen:
                current = self.screens[self.current_screen]
                if hasattr(current, "on_hide"):
                    current.on_hide()  # type: ignore[attr-defined]
                if add_history and self.current_screen not in {"LockScreen"}:
                    self.history.append(self.current_screen)
                    self.history = self.history[-20:]
            self.current_screen = name
            screen = self.screens[name]
            screen.tkraise()
            if hasattr(screen, "on_show"):
                screen.on_show()  # type: ignore[attr-defined]
            self.activity()
        except Exception as exc:
            LOGGER.exception("Screen navigation failed")
            messagebox.showerror("Python Smartwatch", f"Could not open screen.\n\n{exc}")

    def finish_boot(self) -> None:
        target = "LockScreen" if self.state.locked else "HomeScreen"
        self.history.clear()
        self.show_screen(target, add_history=False)

    def go_back(self) -> None:
        while self.history:
            name = self.history.pop()
            if name in self.screens:
                self.show_screen(name, add_history=False)
                return
        self.show_screen("HomeScreen", add_history=False)

    def home(self) -> None:
        self.history.clear()
        self.show_screen("HomeScreen", add_history=False)

    def lock(self) -> None:
        self.state.locked = True
        self.store.save(self.state)
        self.show_screen("LockScreen", add_history=False)

    def unlock(self) -> None:
        self.state.locked = False
        self.store.save(self.state)
        self.history.clear()
        self.show_screen("HomeScreen", add_history=False)

    def activity(self, *_: object) -> None:
        self.power.timeout_seconds = self.state.settings.screen_timeout_seconds
        self.power.activity()
        self.screen_container.configure(bg=self.theme.colours["bg"])

    def _power_tick(self) -> None:
        if self.power.should_sleep():
            self.power.sleep()
            self.screen_container.configure(bg="black")
            self.lock()
        self.after(1000, self._power_tick)

    def _bind_controls(self) -> None:
        self.bind_all("<Home>", lambda _e: self.home())
        self.bind_all("<Escape>", self._escape)
        self.bind_all("<F11>", lambda _e: self.toggle_fullscreen())
        self.bind_all("<Left>", lambda _e: self.navigate_main(-1))
        self.bind_all("<Right>", lambda _e: self.navigate_main(1))
        self.bind_all("<Up>", lambda _e: self.show_screen("QuickSettingsScreen"))
        self.bind_all("<Down>", lambda _e: self.show_screen("NotificationsScreen"))
        self.bind_all("<space>", lambda _e: self.side_button())
        self.bind_all("<Key-l>", lambda _e: self.lock())
        self.screen_container.bind("<ButtonPress-1>", self._touch_press, add="+")
        self.screen_container.bind("<ButtonRelease-1>", self._touch_release, add="+")
        self.bind_all("<Any-KeyPress>", self.activity, add="+")

    def _escape(self, _event: tk.Event) -> None:
        if self.fullscreen:
            self.toggle_fullscreen()
        else:
            self.go_back()

    def toggle_fullscreen(self) -> None:
        self.fullscreen = not self.fullscreen
        self.attributes("-fullscreen", self.fullscreen)

    def side_button(self) -> None:
        if self.current_screen == "LockScreen":
            self.power.wake()
        else:
            self.home()

    def navigate_main(self, direction: int) -> None:
        current = self.current_screen if self.current_screen in self.MAIN_SCREENS else "HomeScreen"
        index = self.MAIN_SCREENS.index(current)
        self.show_screen(self.MAIN_SCREENS[(index + direction) % len(self.MAIN_SCREENS)])

    def _touch_press(self, event: tk.Event) -> None:
        self.activity()
        self._touch_start = (event.x_root, event.y_root, event.time)

    def _touch_release(self, event: tk.Event) -> None:
        if not self._touch_start:
            return
        x, y, started = self._touch_start
        dx, dy = event.x_root - x, event.y_root - y
        duration = event.time - started
        self._touch_start = None
        if duration >= 700 and abs(dx) < 20 and abs(dy) < 20:
            self.events.publish("long_press", screen=self.current_screen)
        elif abs(dx) > 60 and abs(dx) > abs(dy):
            self.navigate_main(-1 if dx > 0 else 1)
        elif abs(dy) > 60:
            self.show_screen("QuickSettingsScreen" if dy > 0 else "NotificationsScreen")

    def refresh_all(self) -> None:
        self.theme.set(self.state.settings.theme)
        self.configure(bg=self.theme.colours["bg"])
        for screen in self.screens.values():
            if hasattr(screen, "rebuild"):
                screen.rebuild()  # type: ignore[attr-defined]
        if self.current_screen:
            self.screens[self.current_screen].tkraise()
            self.screens[self.current_screen].on_show()  # type: ignore[attr-defined]

    def save_state(self) -> None:
        self.connectivity.sync_from_settings(self.state.settings)
        self.hardware.set_brightness(self.state.settings.brightness)
        self.store.save(self.state)

    def _build_simulator_panel(self, parent: tk.Frame) -> None:
        hw = self.hardware
        if not isinstance(hw, SimulatedHardware):
            return
        fg, bg = "white", "#20262e"
        tk.Label(parent, text="Hardware Simulator", bg=bg, fg=fg, font=("Helvetica", 15, "bold")).pack(pady=(14, 8))

        scenario = tk.StringVar(value="Normal")
        tk.OptionMenu(parent, scenario, "Normal", "Low battery", "Charging", "Sensor failure").pack(fill="x", padx=12)
        tk.Button(parent, text="Apply scenario", command=lambda: (hw.apply_scenario(scenario.get()), self._refresh_current())).pack(fill="x", padx=12, pady=6)

        def slider(label: str, start: int, end: int, initial: int, callback: object) -> None:
            tk.Label(parent, text=label, bg=bg, fg=fg).pack(anchor="w", padx=12)
            scale = tk.Scale(parent, from_=start, to=end, orient="horizontal", bg=bg, fg=fg, highlightthickness=0, command=callback)
            scale.set(initial)
            scale.pack(fill="x", padx=12)

        snap = hw.read_sensors()
        slider("Battery %", 0, 100, snap.battery_percent, lambda value: (hw.update(battery_percent=int(float(value))), self._refresh_current()))
        slider("Heart rate", 30, 200, snap.heart_rate_bpm or 72, lambda value: (hw.update(heart_rate_bpm=int(float(value))), self._refresh_current()))
        slider("Steps", 0, 20000, snap.steps, lambda value: (hw.update(steps=int(float(value))), self._refresh_current()))
        charging = tk.BooleanVar(value=snap.charging)
        tk.Checkbutton(parent, text="Charging", variable=charging, bg=bg, fg=fg, selectcolor="#404852", command=lambda: (hw.update(charging=charging.get()), self._refresh_current())).pack(anchor="w", padx=12, pady=5)
        tk.Button(parent, text="Side button", command=self.side_button).pack(fill="x", padx=12, pady=4)
        tk.Button(parent, text="Lock", command=self.lock).pack(fill="x", padx=12, pady=4)
        tk.Button(parent, text="Vibrate", command=lambda: hw.vibrate(250)).pack(fill="x", padx=12, pady=4)

    def _refresh_current(self) -> None:
        if self.current_screen and hasattr(self.screens[self.current_screen], "on_show"):
            self.screens[self.current_screen].on_show()  # type: ignore[attr-defined]

    def shutdown(self) -> None:
        try:
            self.save_state()
            self.hardware.close()
        finally:
            self.destroy()
