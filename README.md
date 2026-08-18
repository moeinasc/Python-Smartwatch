⌚ Python Smartwatch OS v3.1
A Modern Smartwatch Operating System Simulation Built with Python & Tkinter

screenshots/splashscreen.png

A feature-rich smartwatch operating system simulator written entirely in Python using Tkinter.

Designed for desktop simulation, Raspberry Pi prototyping, and future migration to embedded hardware platforms.

🚀 Overview

Python Smartwatch OS is a modular smartwatch operating system written in Python.

The project started as a simple smartwatch interface and has evolved into a complete smartwatch simulation framework featuring:

Modern UI
Hardware simulator
Persistent settings
Health tracking
Notifications
Connectivity management
Diagnostics tools
Raspberry Pi hardware abstraction
Splash screen and animated boot sequence

The architecture is designed so the same core logic can later be ported to physical smartwatch hardware.

✨ Features
⌚ Watch Core

✅ Animated Boot Splash Screen

Smartwatch OS logo
Boot progress animation
Service loading simulation

✅ Home Screen

Digital clock
Date display
Battery indicator
Connectivity status
Health summary

✅ Lock Screen

Secure watch lock
Notification preview

✅ App Launcher

Modern icon-based layout
Touch-friendly interface
❤️ Health Tracking
Heart Rate Monitor (simulated)
Step Counter
Activity Statistics
Sensor Status Monitoring

Health values are simulated in desktop mode and are intended for development purposes.

🌤 Weather
Current Temperature
Weather Status
Location Display
Weather Service Architecture
📩 Messaging & Notifications
Messages
Simulated Messages
Notification Generation
Message History
Notification Centre
Unread Counter
Mark as Read
Clear Notifications
⏱ Productivity Tools
Timer
Multiple Presets
Start / Pause
Countdown Alerts
Stopwatch
High Accuracy Timer
Start / Pause / Reset
Alarm
Alarm Scheduling
Vibration Simulation
Notification Triggering
⚙️ Quick Settings
Wi-Fi Toggle
Bluetooth Toggle
Sound Control
Vibration Control
Do Not Disturb Mode
Battery Saver Mode
Brightness Slider
📶 Connectivity
Supported Services
Wi-Fi (Simulated)
Bluetooth (Simulated)
Mobile Data (Simulated)

Architecture is prepared for future implementation of:

BLE Pairing
Phone Companion App
Notification Synchronisation
🔋 Power Management
Automatic Screen Timeout
Sleep Mode
Wake Events
Battery Monitoring
Power Saving Options
🛠 Diagnostics & Engineering Tools
Smartwatch Diagnostics
Hardware Information
Battery State
Sensor Status
CPU Statistics
Memory Statistics
System Self-Test

Designed especially for Raspberry Pi deployment and hardware troubleshooting.

🎨 Interface Improvements in v3.1
Modern UI

✅ Dark Theme

✅ Light Theme

✅ Responsive Design

✅ Scalable Layout

✅ Round Display Safe Area Support

✅ Modern Icon Library

Included Icons
Home
Apps
Health
Weather
Messages
Alarm
Timer
Stopwatch
Notifications
Settings
Connectivity
Diagnostics
Lock
Quick Settings
Battery

And more.

🖥 Screenshots
Boot Splash Screen

screenshots/splashscreen.png

Home Screen

screenshots/home.png

App Launcher

screenshots/apps.png

Health App

screenshots/health.png

Quick Settings

screenshots/quicksettings.png

Diagnostics

screenshots/diagnostics.png

🛠 Installation
Requirements
Software
Python 3.10+
Tkinter
Pillow
Optional
psutil

For enhanced diagnostics.

Install Dependencies
Shell
1
pip install pillow psutil
Show more lines
📥 Clone Repository
Shell
1
git clone https://github.com/moeinascari/python-smartwatch-os.git
2
cd python-smartwatch-os
Show more lines
▶️ Run Smartwatch OS
Standard Mode
Shell
1
python main.py
Show more lines
Simulator Mode
Shell
1
python main.py --simulator
Show more lines
Fullscreen Mode
Shell
1
python main.py --fullscreen
Show more lines
Raspberry Pi Mode
Shell
1
python main.py --hardware raspberry-pi --fullscreen
Show more lines
🎮 Navigation
Keyboard Controls
Key	ActionHome	Go Home
Esc	Back
F11	Fullscreen
Left	Previous Screen
Right	Next Screen
Up	Quick Settings
Down	Notifications
Space	Side Button
L	Lock Screen
Touch Gestures
Swipe Left / Right

Move between watch screens.

Swipe Down

Open Quick Settings.

Swipe Up

Open Notifications.

Long Press

Open contextual actions.

🏗 Project Architecture
Plain Text
1
python-smartwatch-os/
2
│
3
├── main.py
4
├── config.json
5
│
6
├── assets/
7
│ └── icons/
8
│
9
├── apps/
10
│ ├── home.py
11
│ ├── health.py
12
│ ├── weather.py
13
│ ├── messages.py
14
│ ├── timer.py
15
│ ├── stopwatch.py
16
│ ├── alarm.py
17
│ └── diagnostics.py
18
│
19
├── core/
20
│ ├── state.py
21
│ ├── scheduler.py
22
│ ├── event_bus.py
23
│ └── power_manager.py
24
│
25
├── hardware/
26
│ ├── simulator.py
27
│ └── raspberry_pi.py
28
│
29
├── services/
30
│ ├── storage.py
31
│ ├── notifications.py
32
│ ├── connectivity.py
33
│ └── weather.py
34
│
35
└── ui/
36
├── controller.py
37
├── theme.py
38
└── assets.py
Show more lines
🔬 Hardware Roadmap
Desktop Simulator ✅

Current platform.

Raspberry Pi Prototype ✅

Planned Hardware:

Raspberry Pi Zero 2 W
Touchscreen Display
Haptic Motor
Battery Management Circuit
Accelerometer
Heart Rate Sensor
Embedded Smartwatch Edition

Future migration path:

ESP32-S3
MicroPython
LVGL GUI
BLE Connectivity
Low Power Modes
🌟 Future Development
Version 3.2
Watch Face Designer
Animated Widgets
App Store Framework
Multi-language Support
Version 4.0
BLE Phone Synchronisation
OTA Updates
Cloud Backup
Widget Framework
Real Sensor Support
👨‍💻 Technologies
Python
Tkinter
Pillow
JSON
Object-Oriented Design
Raspberry Pi Integration
Hardware Abstraction Layer
🤝 Contributing

Contributions are welcome!

Steps
Fork the repository
Create a feature branch
Shell
1
git checkout -b feature/my-feature
Show more lines
Commit changes
Shell
1
git commit -m "Add new feature"
2
``
Show more lines
Push branch
Shell
1
git push origin feature/my-feature
Show more lines
Open a Pull Request
📜 License

Released under the MIT License.

⭐ Support the Project

If you enjoy this project, please consider:

⭐ Starring the repository

🐛 Reporting bugs

💡 Suggesting new features

🤝 Contributing code

Developer

Moein Ascari

System Engineer | Python Developer | Network & Automation Enthusiast

"Building an open-source smartwatch OS entirely in Python."
