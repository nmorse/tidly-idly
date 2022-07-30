# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
import math
import time
import displayio
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.roundrect import RoundRect
from adafruit_display_shapes.line import Line
from adafruit_display_shapes.polygon import Polygon

# use built in display (PyPortal, PyGamer, PyBadge, CLUE, etc.)
# see guide for setting up external displays (TFT / OLED breakouts, RGB matrices, etc.)
# https://learn.adafruit.com/circuitpython-display-support-using-displayio/display-and-display-bus
display = board.DISPLAY

# Make the display context
splash = displayio.Group()
time.sleep(0.5)
display.show(splash)

# Make a background color fill
color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF
bg_sprite = displayio.TileGrid(color_bitmap, x=0, y=0, pixel_shader=color_palette)
splash.append(bg_sprite)
##########################################################################

def tidal (ax, ay, bx, by, highToLow) :
    print(ax, ay, bx, by)
    cosOffset = math.pi
    if highToLow > 0:
        cosOffset = 0
    rangeX = bx - ax
    rangeY = (ay - by) / 2 * highToLow
    topY = ay
    if by < ay:
        topY = by
    for x in range(ax, bx):
        splash.append(Line(x, 
        int((math.cos(cosOffset + ((x - ax)/rangeX)*math.pi)+1)*rangeY)+topY, 
        x+1, 
        int((math.cos(cosOffset + ((x+1 - ax)/rangeX)*math.pi)+1)*rangeY)+topY, 0x000000))


# night time 
rect = Rect(60, 0, 50, display.height, fill=0x999999, outline=0x666666)
splash.append(rect)

rect2 = Rect(210, 0, 50, display.height, fill=0x999999, outline=0x666666)
splash.append(rect2)

# rising and falling tides
tidal(0, 100, 40, 20, 1)
tidal(40, 20, 80, 90, -1)
tidal(80, 90, 122, 10, 1)
tidal(122, 10, 160, 110, -1)

tidal(160, 110, 200, 10, 1)
tidal(200, 10, 240, 90, -1)
tidal(240, 90, 282, 15, 1)
tidal(282, 15, 320, 90, -1)

time.sleep(2.5)
display.refresh()
while True:
    time.sleep(2.5)
