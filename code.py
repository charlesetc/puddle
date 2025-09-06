# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import math
import time

import adafruit_sharpmemorydisplay
import board
import busio
import digitalio
import displayio
from adafruit_display_text import label

# from font_free_mono_8 import FONT
from terminalio import FONT

SQUARE_SIZE = 16
MARGIN = 8
ANIMATION_DELAY = 0.01

spi = busio.SPI(board.GP18, MOSI=board.GP19)
scs = digitalio.DigitalInOut(board.GP17)

button = digitalio.DigitalInOut(board.GP20)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP  # Use internal pull-up resistor

display = adafruit_sharpmemorydisplay.SharpMemoryDisplay(
    spi,
    scs,
    144,
    168,
)

display.fill(1)
main_group = displayio.Group()
display.root_group = main_group

text_to_display = "Hello, World!"
# text_color = 0x111111
text_color = 0

# Create the label object using the imported font
text_area = label.Label(FONT, text=text_to_display, color=text_color)
text_area.x = 10
text_area.y = 10
main_group.append(text_area)


display.show()

# frame = 0

# while True:
#     # display.text("Hello, World!", 10, 10, 0)
#     # display.show()
#     time.sleep(1)

#     display.fill_rect(
#         display.width - 10 - SQUARE_SIZE,
#         display.height - 10 - SQUARE_SIZE,
#         SQUARE_SIZE,
#         SQUARE_SIZE,
#         0,
#     )  # Draw square
#     display.show()
#     # time.sleep(ANIMATION_DELAY)

#     print("")
#     print("HELLO")

#     frame += 1
