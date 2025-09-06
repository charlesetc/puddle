# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
import json
import time

import adafruit_requests
import board
import busio
import digitalio
import displayio
import framebufferio
import rotaryio
import sharpdisplay
import socketpool
import wifi
from adafruit_datetime import datetime, timedelta
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


apps = [
    "clock",
    "artwork",
    # "weather",
    # "news",
    # "lobsters"
]


class Controller:
    def __init__(self):
        self.state = "menu"
        self.connect_wifi("Fios-gLwY5", "stem65fan74grew")
        self.setup_reference_time()

        # Release any existing displays before claiming pins
        displayio.release_displays()

        # Initialize SPI
        spi = busio.SPI(board.GP18, MOSI=board.GP19)

        # --- Button Setup ---
        # The button will be connected to GP20 and Ground
        self.button = digitalio.DigitalInOut(board.GP20)
        self.button.direction = digitalio.Direction.INPUT
        self.button.pull = digitalio.Pull.UP  # Use internal pull-up resistor

        self.escape = digitalio.DigitalInOut(board.GP16)
        self.escape.direction = digitalio.Direction.INPUT
        self.escape.pull = digitalio.Pull.UP  # Use internal pull-up resistor

        self.encoder = rotaryio.IncrementalEncoder(board.GP0, board.GP1)

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
        self.display = framebufferio.FramebufferDisplay(framebuffer)

        # Create a group to hold the label
        self.main_group = displayio.Group()

        self.main_group.append(self.create_background(self.display, 0xFFFFFF))

        # Create the label
        self.text_label = Label(
            font=FONT,
            text="Hello\nWorld!",
            x=36,  # Adjusted X position to center for 144 width
            y=76,  # Adjusted Y position to center for 168 height
            scale=2,
            line_spacing=1.2,
            color=0x000000,
        )

        # Add the label to the group
        self.main_group.append(self.text_label)

        # Set the group as the root to display it
        self.display.root_group = self.main_group

    def connect_wifi(self, ssid, password):
        print("Connecting to WiFi...")
        wifi.radio.connect(ssid, password)
        print(f"Connected! {wifi.radio.ipv4_address}")

    @cache
    def socketpool(self):
        # Make sure WiFi is connected before calling this method
        return socketpool.SocketPool(wifi.radio)

    @cache
    def requests(self):
        return adafruit_requests.Session(self.socketpool())

    def setup_reference_time(self):
        try:
            response = self.requests().get(
                "http://worldtimeapi.org/api/timezone/Etc/UTC"
            )
            time_data = response.json()

            datetime_str = time_data["datetime"]
            dt = datetime.fromisoformat(datetime_str)
            self.reference_time = [dt, time.time()]

            print(f"Finished setting reference time: {dt}")
        except Exception as e:
            print(f"Error getting time: {e}")
        finally:
            if "response" in locals():
                response.close()

    def get_time(self):
        if not hasattr(self, "reference_time"):
            return "no ref time"

        dt, at_time = self.reference_time
        elapsed = time.time() - at_time

        new_dt = datetime.fromtimestamp(dt.timestamp() + int(elapsed))
        # convert to local time (Eastern)
        new_dt = new_dt - timedelta(hours=4)
        return f"{new_dt.hour:02}:{new_dt.minute:02}:{new_dt.second:02}"

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
        if self.state == "menu":
            self.update_menu()
        elif self.state == "clock":
            self.update_clock()
        elif self.state == "artwork":
            self.update_artwork()

    def update_clock(self):
        self.text_label.text = self.get_time()

    def update_artwork(self):
        self.text_label.text = "Art!"

    def update_menu(self):
        if not self.button.value:
            self.text_label.text = self.get_time()
        elif not self.escape.value:
            self.text_label.text = "Escape!"
            self.encoder.position = 0
        else:
            self.text_label.text = str(self.encoder.position)
        self.display.refresh()


controller = Controller()
controller.loop()