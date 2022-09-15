# !/usr/bin/env python
# coding: utf-8

__version__ = "v1.0"
__author__ = "Aditya Marathe"

import os
import sys

import json
import requests
from numpy import loadtxt

import time
import datetime

import tkinter as tk
from tkinter import messagebox

from PIL import Image
from PIL import ImageTk

from dotenv import load_dotenv

# Directories
RES_DIR = "window/res/"
BG_DIR = RES_DIR + "bg/"
ICON_DIR = RES_DIR + "icons/"

# Enviornment variables
load_dotenv(RES_DIR + ".env")
API_KEY = os.getenv("API_KEY")

# Units settings
UNITS = "metric"

# UI: Fonts
TITLE_FONT = ("Microsoft JhengHei Light", 30)
SUBTITLE_FONT = ("Microsoft JhengHei Light", 20)
TEXT_FONT = ("Microsoft YaHei UI", 10)
BOLD_FONT = ("Microsoft YaHei UI", 10, "bold")

# UI: Colours
DAY_BG_COLOUR = "#4472C4"
DAY_FG_COLOUR = "#000000"

NIGHT_BG_COLOUR = "#203864"
NIGHT_FG_COLOUR = "#FFFFFF"


def get_weather(location="London") -> int | dict:
    """Gets the weather at any location (city name).

    Notes:
        Uses the `requests` module to get weather information from OpenWeather API.

    Args:
        location (str, optional): Location. Defaults to "London".

    Returns:
        int | dict: Weather information. 
                    Returns 0, if location not found. 
                    Returns -1, if no internet connection.
    
    """
    url = f"http://api.openweathermap.org/data/2.5/weather?" \
          f"appid={API_KEY}&q={location}&units={UNITS}"
    
    try:
        api_response = requests.get(url).json()
    except requests.exceptions.ConnectionError:
        return -1

    output = dict()

    if api_response["cod"] == "404":
        return 0

    output["temperature"] = str(round(api_response["main"]["temp"]))
    output["feels_like"] = str(round(api_response["main"]["feels_like"]))
    output["humidity"] = str(round(api_response["main"]["humidity"]))
    output["wind_speed"] = str(round(api_response["wind"]["speed"]))
    output["wind_deg"] = str(round(api_response["wind"]["deg"]))
    
    output["location"] = api_response["name"] + ", " + api_response["sys"]["country"]
    output["description"] = api_response["weather"][0]["description"].title()

    output["icon"] = api_response["weather"][0]["icon"]

    return output


def main(*args, **kwargs) -> int:
    """Window Weather App.

    Returns:
        int: Exit code.
    """
    root = tk.Tk()
        
    # Display Info
    SCREEN_WIDTH = root.winfo_screenwidth()
    SCREEN_HEIGHT = root.winfo_screenheight()

    # Window: Size, Placement
    WIDTH, HEIGHT = 500, 535
    X = (SCREEN_WIDTH - WIDTH) // 2
    Y = (SCREEN_HEIGHT - HEIGHT) // 3

    root.title(f" Window Weather")
    root.geometry(f"{WIDTH}x{HEIGHT}+{X}+{Y}")
    root.resizable(False, False)

    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=100)
    root.grid_columnconfigure(0, weight=1)

    root["bg"] = "white"

    #
    # data = sorted(loadtxt(RES_DIR + "city_names.csv", 
    #           delimiter = "\n", dtype=str)[1:].tolist())
    #

    # Window: Colours
    bg_colour = DAY_BG_COLOUR
    fg_colour = DAY_FG_COLOUR

    # Window: Variables
    time_text = tk.StringVar()
    greeting_text = tk.StringVar()
    location = tk.StringVar()
    temperature = tk.StringVar()
    feels_like = tk.StringVar()
    humidity = tk.StringVar()
    wind_speed = tk.StringVar()
    wind_deg = tk.StringVar()
    description = tk.StringVar()

    # Window: Background
    bg_label = tk.Label(root, bd=0)
    bg_label.grid(row=0, column=0, sticky=tk.N)

    # Window: Container
    container = tk.Frame(root, highlightbackground="white", highlightthickness=2)
    container.grid(row=0, column=0, sticky=tk.NSEW, padx=100, pady=90)

    container.grid_rowconfigure(0, weight=0)
    container.grid_rowconfigure(1, weight=0)
    container.grid_rowconfigure(2, weight=0)
    container.grid_rowconfigure(3, weight=2)
    container.grid_rowconfigure(4, weight=1)
    container.grid_rowconfigure(5, weight=1)
    container.grid_rowconfigure(6, weight=0)

    container.grid_columnconfigure(0, weight=1)
    container.grid_columnconfigure(1, weight=1)
    
    tk.Label(
        container, textvariable=location, font=SUBTITLE_FONT, wraplength=280
    ).grid(row=0, columnspan=2, padx=10, pady=(10, 0))
    
    # Window: Container: Small Container
    small_container = tk.Frame(container)
    small_container.grid(row=1, columnspan=2)
    icon_label = tk.Label(small_container)
    icon_label.grid(row=1, column=0, sticky=tk.E)
    tk.Label(
        small_container, textvariable=temperature, font=TITLE_FONT
    ).grid(row=1, column=1, sticky=tk.W)
    
    # Window: Container
    tk.Label(
        container, text="Feels like", font=BOLD_FONT
    ).grid(row=2, column=0, sticky=tk.E)
    tk.Label(
        container, textvariable=feels_like, font=BOLD_FONT
    ).grid(row=2, column=1, sticky=tk.W)

    tk.Label(
        container, textvariable=description, font=SUBTITLE_FONT
    ).grid(row=3, columnspan=2, pady=(0, 10))
    
    tk.Label(
        container, text="Humidity", font=TEXT_FONT
    ).grid(row=4, column=0, sticky=tk.E)
    tk.Label(
        container, textvariable=humidity, font=TEXT_FONT
    ).grid(row=4, column=1, stick=tk.W)

    tk.Label(
        container, text="Wind speed", font=TEXT_FONT
    ).grid(row=5, column=0, sticky=tk.E)
    tk.Label(
        container, textvariable=wind_speed, font=TEXT_FONT
    ).grid(row=5, column=1, stick=tk.W)

    tk.Label(
        container, text="Wind deg.", font=TEXT_FONT
    ).grid(row=6, column=0, sticky=tk.E, pady=(0, 10))
    tk.Label(
        container, textvariable=wind_deg, font=TEXT_FONT
    ).grid(row=6, column=1, stick=tk.W, pady=(0, 10))

    # Window: Bottom Bar
    bottom_bar = tk.Frame(root)
    bottom_bar.grid(row=1, column=0, sticky=tk.NSEW, pady=(2, 0))

    tk.Label(
        bottom_bar, textvariable=greeting_text, font=TEXT_FONT
    ).pack(side=tk.LEFT, padx=10, pady=5)

    tk.Label(
        bottom_bar, textvariable=time_text, font=TEXT_FONT
    ).pack(side=tk.RIGHT, padx=10, pady=5)

    # Reference for later
    children = []
    children.extend(root.winfo_children())
    children.extend(container.winfo_children())
    children.extend(small_container.winfo_children())
    children.extend(bottom_bar.winfo_children())

    # Window: Auto Updates
    def update_weather() -> int:
        # Weather Updates
        weather = get_weather()

        if not weather:
            messagebox.showerror("Window Weather: Error!", "Location not found.")
            return -1

        if weather == -1:
            messagebox.showerror("Window Weather: Error!", "No internet connection!")
            return -1

        # UI Updates
        temperature_units = "°C" if UNITS == "metric" else "°F"
        speed_units = " ms\u207b\xb9" if UNITS == "metric" else " mph"

        location.set(weather["location"])
        temperature.set(weather["temperature"] + temperature_units)
        feels_like.set(weather["feels_like"] + temperature_units)
        humidity.set(weather["humidity"] + "%")
        wind_speed.set(weather["wind_speed"] + speed_units)
        wind_deg.set(weather["wind_deg"] + "°")
        description.set(weather["description"])
        icon = weather["icon"]

        image = ImageTk.PhotoImage(Image.open(BG_DIR + icon + ".jpg"))
        bg_label["image"] = image
        bg_label.image = image

        image = ImageTk.PhotoImage(Image.open(ICON_DIR + icon + ".png"))
        icon_label["image"] = image
        icon_label.image = image

        root.iconphoto(False, image)

        time_code = list(icon)[-1]
        if time_code == "d":
            bg_colour = DAY_BG_COLOUR
            fg_colour = DAY_FG_COLOUR
        elif time_code == "n":
            bg_colour = NIGHT_BG_COLOUR
            fg_colour = NIGHT_FG_COLOUR

        for child in children:
            try:
                child["bg"] = bg_colour
                child["fg"] = fg_colour
            except tk.TclError:
                pass

        root.update_idletasks()

        # Loop
        root.after(60_000, update_weather)

        return 0


    def update_bar() -> None:
        current_hour = datetime.datetime.now().hour

        # UI Updates
        if current_hour < 12:
            greeting_text.set("Good Morning")
        elif current_hour < 18:
            greeting_text.set("Good Afternoon")
        elif current_hour < 20:
            greeting_text.set("Good Evening")
        elif current_hour < 24:
            greeting_text.set("Good Night")

        time_text.set(time.strftime("%H:%M:%S"))

        # Loop
        root.after(1_000, update_bar)


    # Window: Updates
    update_bar()

    if update_weather() == -1:
        return -1

    root.mainloop()

    return 0


if __name__ == "__main__":
    sys.exit(main())
