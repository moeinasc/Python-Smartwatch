import tkinter as tk
from tkinter import messagebox, ttk
import time
import random
from PIL import Image, ImageTk
import os

# Initialize Tkinter Root Window
root = tk.Tk()
root.title("Smartwatch OS")
root.geometry("320x320")
root.configure(bg="black")

# ✅ Global variable for screen switching
current_screen = None  

# ✅ Global Settings Variables
brightness = 100  
bluetooth_status = "Connected"
wifi_status = "On"
mobile_data_status = "Off"
power_mode = "Normal"
sound_status = "On"
vibration_status = "On"
theme = "Dark"

# ✅ Safe Image Loading Function
def load_image(filename, size):
    if not os.path.exists(filename):
        print(f"⚠️ Warning: Image not found: {filename}")
        return None  
    try:
        return ImageTk.PhotoImage(Image.open(filename).resize(size))
    except Exception as e:
        print(f"⚠️ Error loading {filename}: {e}")
        return None

# ✅ Load Images
icon_settings = load_image("settings.png", (50, 50))
icon_health = load_image("health.png", (50, 50))
icon_message = load_image("message.png", (50, 50))
icon_weather = load_image("weather.png", (50, 50))

# ✅ Ensure Placeholder Images
if icon_settings is None:
    icon_settings = ImageTk.PhotoImage(Image.new("RGB", (50, 50), "gray"))
if icon_health is None:
    icon_health = ImageTk.PhotoImage(Image.new("RGB", (50, 50), "gray"))
if icon_message is None:
    icon_message = ImageTk.PhotoImage(Image.new("RGB", (50, 50), "gray"))
if icon_weather is None:
    icon_weather = ImageTk.PhotoImage(Image.new("RGB", (50, 50), "gray"))

# ✅ Function to Switch Screens
def switch_screen(new_screen):
    global current_screen
    try:
        if current_screen:
            current_screen.destroy()
        current_screen = new_screen
        current_screen.pack(expand=True, fill="both")
    except Exception as e:
        print(f"⚠️ Error switching screen: {e}")

# 🌟 Splash Screen
def splash_screen():
    splash = tk.Frame(root, bg="black")
    tk.Label(splash, text="⌚ Smartwatch OS", font=("Helvetica", 20, "bold"), fg="cyan", bg="black").pack(expand=True)
    tk.Label(splash, text="The Python Smartwatch OS is loading...", font=("Helvetica", 10, "bold"), fg="white", bg="black").pack(expand=True)
    switch_screen(splash)
    root.after(2000, home_screen)  

# ⌚ Home Screen
def home_screen():
    frame = tk.Frame(root, bg="black")

    def update_time():
        time_label.config(text=time.strftime("%H:%M:%S"))
        frame.after(1000, update_time)

    time_label = tk.Label(frame, text="", font=("Helvetica", 28, "bold"), fg="white", bg="black")
    time_label.pack(pady=10)
    update_time()

    battery_label = tk.Label(frame, text="🔋 85%", font=("Helvetica", 12), fg="green", bg="black")
    battery_label.pack()
    bluetooth_label = tk.Label(frame, text=f"📶 {bluetooth_status}", font=("Helvetica", 12), fg="cyan", bg="black")
    bluetooth_label.pack()

    menu_button = tk.Button(frame, text="🔘 Menu", font=("Helvetica", 14), bg="gray", fg="white", command=apps_menu)
    menu_button.pack(pady=20)

    switch_screen(frame)

# ✅ Define All Apps Before `apps_menu()`
# ❤️ Health App
def health_app():
    frame = tk.Frame(root, bg="black")
    tk.Label(frame, text="💓 Health Stats", font=("Helvetica", 18, "bold"), fg="white", bg="black").pack(pady=10)

    heart_rate = random.randint(60, 100)
    steps = random.randint(1000, 10000)
    calories = random.randint(100, 500)

    tk.Label(frame, text=f"Heart Rate: {heart_rate} bpm", font=("Helvetica", 14), fg="red", bg="black").pack()
    tk.Label(frame, text=f"Steps: {steps}", font=("Helvetica", 14), fg="green", bg="black").pack()
    tk.Label(frame, text=f"Calories: {calories} kcal", font=("Helvetica", 14), fg="orange", bg="black").pack()

    tk.Button(frame, text="⬅ Back", font=("Helvetica", 14), bg="gray", fg="white", command=apps_menu).pack(pady=10)
    switch_screen(frame)

# 📩 Messages App
def messages_app():
    frame = tk.Frame(root, bg="black")
    tk.Label(frame, text="📩 Messages", font=("Helvetica", 18, "bold"), fg="white", bg="black").pack(pady=10)

    messages = ["🔔 Meeting at 10 AM", "📩 New Email", "📱 Missed Call"]
    for msg in messages:
        tk.Label(frame, text=msg, font=("Helvetica", 12), fg="yellow", bg="black").pack(pady=3)

    tk.Button(frame, text="⬅ Back", font=("Helvetica", 14), bg="gray", fg="white", command=apps_menu).pack(pady=10)
    switch_screen(frame)

# ⚙️ Settings App
def settings_app():
    frame = tk.Frame(root, bg="black")
    tk.Label(frame, text="⚙️ Settings", font=("Helvetica", 18, "bold"), fg="white", bg="black").pack(pady=10)

    tk.Button(frame, text="⬅ Back", font=("Helvetica", 14), bg="gray", fg="white", command=apps_menu).pack(pady=10)
    switch_screen(frame)

# 🌤 Weather App
def weather_app():
    frame = tk.Frame(root, bg="black")
    tk.Label(frame, text="🌤 Weather", font=("Helvetica", 18, "bold"), fg="white", bg="black").pack(pady=10)

    temperature = random.randint(10, 35)
    condition = random.choice(["☀ Sunny", "🌧 Rainy", "⛅ Cloudy"])

    tk.Label(frame, text=f"🌡 Temp: {temperature}°C", font=("Helvetica", 14), fg="lightblue", bg="black").pack()
    tk.Label(frame, text=f"{condition}", font=("Helvetica", 14), fg="yellow", bg="black").pack()

    tk.Button(frame, text="⬅ Back", font=("Helvetica", 14), bg="gray", fg="white", command=apps_menu).pack(pady=10)
    switch_screen(frame)

# 📱 Apps Menu (Now After All Functions Are Defined)
def apps_menu():
    frame = tk.Frame(root, bg="black")
    tk.Label(frame, text="Apps", font=("Helvetica", 18, "bold"), fg="white", bg="black").pack(pady=10)

    apps = [
        ("❤️ Health", icon_health, health_app),
        ("📩 Messages", icon_message, messages_app),
        ("⚙️ Settings", icon_settings, settings_app),
        ("🌤 Weather", icon_weather, weather_app),
        ("🏠 Home", None, home_screen)
    ]

    for text, icon, command in apps:
        app_frame = tk.Frame(frame, bg="black")
        if icon:
            icon_label = tk.Label(app_frame, image=icon, bg="black")
            icon_label.pack(side="left", padx=10)
        btn = tk.Button(app_frame, text=text, font=("Helvetica", 14), width=15, bg="gray", fg="white", command=command)
        btn.pack(side="left")
        app_frame.pack(pady=5)

    switch_screen(frame)

# ✅ Start the OS
splash_screen()
root.mainloop()
