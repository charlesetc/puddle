# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
import json

import adafruit_requests
import board
import busio
import digitalio
import displayio
import framebufferio
import sharpdisplay
import socketpool
import wifi
from adafruit_datetime import datetime
from adafruit_display_text.label import Label
from terminalio import FONT


def cache(func):
    """Simple cache decorator that stores function results"""
    cache_dict = {}

    def wrapper(*args, **kwargs):
        # Create a key from arguments
        key = str(args) + str(kwargs)

        # Return cached result if available
        if key in cache_dict:
            return cache_dict[key]

        # Otherwise compute and cache the result
        result = func(*args, **kwargs)
        cache_dict[key] = result
        return result

    return wrapper


class Controller:
    def __init__(self):
        self.connect_wifi("Fios-gLwY5", "stem65fan74grew")

        # Release any existing displays before claiming pins
        displayio.release_displays()

        # Initialize SPI
        spi = busio.SPI(board.GP18, MOSI=board.GP19)

        # --- Button Setup ---
        # The button will be connected to GP20 and Ground
        button = digitalio.DigitalInOut(board.GP20)
        button.direction = digitalio.Direction.INPUT
        button.pull = digitalio.Pull.UP  # Use internal pull-up resistor

        # Create the Sharp Memory Display framebuffer
        # Pass the chip select pin DIRECTLY, not as a DigitalInOut object.
        # Width and height are set to 144x168 as requested.
        framebuffer = sharpdisplay.SharpMemoryFramebuffer(
            spi,
            board.GP17,  # Pass the raw pin here
            144,  # Width
            168,  # Height
        )

        # Create the display object for displayio
        display = framebufferio.FramebufferDisplay(framebuffer)

        # Create a group to hold the label
        main_group = displayio.Group()

        main_group.append(self.create_background(display, 0xFFFFFF))

        # Create the label
        text_label = Label(
            font=FONT,
            text="Hello\nWorld!",
            x=36,  # Adjusted X position to center for 144 width
            y=76,  # Adjusted Y position to center for 168 height
            scale=2,
            line_spacing=1.2,
            color=0x000000,
        )

        # Add the label to the group
        main_group.append(text_label)

        # Set the group as the root to display it
        display.root_group = main_group

        self.button = button
        self.display = display
        self.text_label = text_label

    def connect_wifi(self, ssid, password):
        print("Connecting to WiFi...")
        wifi.radio.connect(ssid, password)
        print(f"Connected! IP: {wifi.radio.ipv4_address}")

    @cache
    def socketpool(self):
        # Make sure WiFi is connected before calling this method
        return socketpool.SocketPool(wifi.radio)

    @cache
    def requests(self):
        return adafruit_requests.Session(self.socketpool())

    def get_time(self):
        try:
            response = self.requests().get(
                "http://worldtimeapi.org/api/timezone/Etc/UTC"
            )
            time_data = response.json()

            datetime_str = time_data["datetime"]
            dt = datetime.fromisoformat(datetime_str)

            return f"{dt.hour:02}:{dt.minute:02}:{dt.second:02}"
        except Exception as e:
            print(f"Error getting time: {e}")
            return "err: time"
        finally:
            if "response" in locals():
                response.close()

    def create_background(self, display, color):
        # Create a bitmap for the background
        bitmap = displayio.Bitmap(display.width, display.height, 1)
        palette = displayio.Palette(1)
        palette[0] = color

        # Create and return a TileGrid to display the bitmap
        background = displayio.TileGrid(bitmap, pixel_shader=palette, x=0, y=0)
        return background

    def loop(self):
        # The display will continue to show the image.
        # An empty loop can keep the program from exiting.
        while True:
            self.update()

    def update(self):
        if self.button.value:
            self.text_label.text = "Hello\nWorld!"
        else:
            self.text_label.text = self.get_time()
        self.display.refresh()


controller = Controller()
controller.loop()