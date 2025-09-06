# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import math
import time

import adafruit_sharpmemorydisplay
import board
import busio
import digitalio

# --- Constants for Animation ---
SQUARE_SIZE = 2
MARGIN = 8
# Control the speed of the animation (smaller is faster)
ANIMATION_DELAY = 0.01

# --- Pin Definitions & SPI Setup ---
# Initialize SPI bus and control pins using specific Pico W GPIO pins
spi = busio.SPI(board.GP18, MOSI=board.GP19)
scs = digitalio.DigitalInOut(board.GP17)

# --- Button Setup ---
# The button will be connected to GP20 and Ground
button = digitalio.DigitalInOut(board.GP20)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP  # Use internal pull-up resistor

# --- Display Setup ---
# Create the displayio display object
# IMPORTANT: Use the correct size for your 1.3" 168x144 display
# We also add a baudrate argument to slow down the SPI speed, which often
# fixes display corruption issues (like seeing random lines).
display = adafruit_sharpmemorydisplay.SharpMemoryDisplay(
    spi,
    scs,
    144,
    168,  #  baudrate=1000000
)

# --- Calculate Animation Boundaries ---
# The min and max coordinates for the top-left corner of the square
x_min = MARGIN
y_min = MARGIN
x_max = display.width - MARGIN - SQUARE_SIZE
y_max = display.height - MARGIN - SQUARE_SIZE

# --- Animation State Variables ---
# Starting position for the square
x = x_min
y = y_min
# Store previous position to erase the old square
prev_x = x
prev_y = y


frame = 0

display.fill(1)  # Clear screen to white
display.show()
while True:
    if not button.value:
        # If button is pressed, reset animation
        frame = 0
        display.fill(1)  # Clear screen to white
        display.show()
        time.sleep(0.1)  # Debounce delay

        # Update position using sine wave functions
    x = int((x_max - x_min) / 2 * math.sin(frame * 0.1) + (x_max + x_min) / 2)
    y = int((y_max - y_min) / 2 * math.sin(frame * 0.15) + (y_max + y_min) / 2)

    display.fill_rect(x, y, SQUARE_SIZE, SQUARE_SIZE, 0)  # Draw square
    # display.pixel(x, y, 0)
    display.show()
        # time.sleep(ANIMATION_DELAY)

    frame += 1
