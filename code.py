# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
import board
import busio
import displayio
import framebufferio
import sharpdisplay
from adafruit_display_text.label import Label
from terminalio import FONT

# Release any existing displays before claiming pins
displayio.release_displays()


# Initialize SPI
spi = busio.SPI(board.GP18, MOSI=board.GP19)


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

# Create the label
text_label = Label(
    font=FONT,
    text="Hello\nWorld!",
    x=36,  # Adjusted X position to center for 144 width
    y=76,  # Adjusted Y position to center for 168 height
    scale=2,
    line_spacing=1.2,
    color=0xFFFFFF,
)

# Add the label to the group
main_group.append(text_label)

# Set the group as the root to display it
display.root_group = main_group

print("DONE")

# The display will continue to show the image.
# An empty loop can keep the program from exiting.
while True:
    pass
