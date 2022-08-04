# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# import board
import math
import time
import json
tideData = []
dayNumber = 216.0
zoomDays = 2
with open('tides.json', 'r') as f:
  tideData = json.load(f)
sunData = []
with open('sun.json', 'r') as f:
  sunData = json.load(f)

import displayio
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.roundrect import RoundRect
from adafruit_display_shapes.line import Line
from adafruit_display_shapes.polygon import Polygon
from adafruit_magtag.magtag import MagTag
magtag = MagTag()
# use built in display (PyPortal, PyGamer, PyBadge, CLUE, etc.)
# see guide for setting up external displays (TFT / OLED breakouts, RGB matrices, etc.)
# https://learn.adafruit.com/circuitpython-display-support-using-displayio/display-and-display-bus
# # # display = board.DISPLAY

# # # # Make the display context
# # # splash = displayio.Group()
# # # time.sleep(1.5)
# # # display.show(splash)

# Make a background color fill
color_bitmap = displayio.Bitmap(magtag.graphics.display.width, magtag.graphics.display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF
bg_sprite = displayio.TileGrid(color_bitmap, x=0, y=0, pixel_shader=color_palette)
magtag.graphics.splash.append(bg_sprite)
##########################################################################

# tidal takes pixel coords and draws a cosine curve profile from pt. a to b
def tidal (ax, ay, bx, by, highToLow) :
    print(ax, ay, bx, by, highToLow)
    cosOffset = math.pi
    if highToLow > 0:
        cosOffset = 0
    rangeX = bx - ax
    rangeY = (by - ay) * highToLow * -1 / 2
    topY = ay
    if by < ay:
        topY = by
    for x in range(ax, bx):
        magtag.graphics.splash.append(Line(x,
        int((math.cos(cosOffset + ((x - ax)/rangeX)*math.pi)+1)*rangeY)+topY,
        x+1,
        int((math.cos(cosOffset + ((x+1 - ax)/rangeX)*math.pi)+1)*rangeY)+topY, 0x000000))


def dispFilter(e):
    return e[0] >= (dayNumber - 0.3) and e[0] < (dayNumber + zoomDays + 0.3)

# night time
nightDay = filter(dispFilter, sunData)
# # # rising and falling tides
startX = 0
for dispD in nightDay:
    endX = (dispD[0] - dayNumber) * 300.0 / zoomDays
    # print(dir)
    if not startX == 0:
        rect2 = Rect(int(startX), 0, int(endX-startX), magtag.graphics.display.height, fill=0x999999, outline=0x999999)
        magtag.graphics.splash.append(rect2)
    dir = 1
    startX = (dispD[0] - dayNumber) * 300.0 / zoomDays



dispDay = filter(dispFilter, tideData)
# # # rising and falling tides
dir = 0
startX = 0
startY = 0
for dispD in dispDay:
    endX = (dispD[0] - dayNumber) * 300.0 / zoomDays
    endY = (14.0 - dispD[4] * -1) * 10 - 130
    # print(dir)
    if not dir == 0:
        tidal(int(startX), int(startY), int(endX), int(endY), dir)
    dir = 1
    if dispD[6] == "L":
        dir = -1
    startX = (dispD[0] - dayNumber) * 300.0 / zoomDays
    startY = (14.0 - dispD[4] * -1) * 10 - 130

# # tidal(0, 120, 40, 20, 1)
# # tidal(40, 20, 80, 90, -1)
# # tidal(80, 90, 122, 10, 1)
# # tidal(122, 10, 160, 110, -1)

# # tidal(160, 110, 200, 10, 1)
# # tidal(200, 10, 240, 90, -1)
# # tidal(240, 90, 282, 15, 1)
# # tidal(282, 15, 320, 90, -1)

# magtag.add_text(
#     text_position=(
#         148,
#         (magtag.graphics.display.height // 2) - 1,
#     ),
#     text_scale=1,
# )
# magtag.set_text("08/02", 0)
# magtag.add_text(
#     text_position=(
#         130,
#         magtag.graphics.display.height - 7,
#     ),
#     text_scale=1,
# )
# magtag.set_text("12:03 -0.3\"", 1)
t2 = magtag.add_text(
    text_position=(
        180,
        3,
    ),
    text_scale=1,
)
magtag.set_text("7:28 11.2\"", t2)
# magtag.graphics.display.refresh()
while True:
    time.sleep(2.5)
