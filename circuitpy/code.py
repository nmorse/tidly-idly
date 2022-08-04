import math
import time
import json
tideData = []
dayNumber = 216.0
zoomDays = 3
with open('tides.json', 'r') as f:
  tideData = json.load(f)
sunData = []
with open('sun.json', 'r') as f:
  sunData = json.load(f)

import displayio
from adafruit_display_shapes.rect import Rect
# from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.line import Line
from adafruit_magtag.magtag import MagTag
magtag = MagTag()

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
    for x in range(ax, bx, 1):
        magtag.graphics.splash.append(Line(x,
        int((math.cos(cosOffset + ((x - ax)/rangeX)*math.pi)+1)*rangeY)+topY,
        x+1,
        int((math.cos(cosOffset + ((x+1 - ax)/rangeX)*math.pi)+1)*rangeY)+topY, 0x000000))

def dayToPix(d):
    return (d - dayNumber) * 300.0 / zoomDays

def sunFilter(e):
    return e[0] >= dayNumber and e[0] < (dayNumber + zoomDays +0.5)

# night time, day time
startX = 0
endX = 0
for e in filter(sunFilter, sunData):
    print(e)
    if e[3] == "R": # end of night
        endX = dayToPix(e[0])
        dateTxt = magtag.add_text(
            text_position=(
                int(dayToPix(e[0])),
                122,
            ),
            text_scale=1,
        )
        magtag.set_text(e[1], dateTxt)
    if e[3] == "S":
        startX = dayToPix(e[0])
    if not endX == 0 and e[3] == "R":
        print("night rectangle", int(startX), 0, int(endX-startX), magtag.graphics.display.height)
        magtag.graphics.splash.append(Rect(int(startX), 0, int(endX-startX), magtag.graphics.display.height, fill=0x999999, outline=0x999999))

# # rising and falling tides
def tideFilter(e):
    return e[0] >= (dayNumber - 0.3) and e[0] < (dayNumber + zoomDays + 0.3)

maxTideFt = 11.5
minTideFt = -1.7
t2pFactor = magtag.graphics.display.height / (maxTideFt - minTideFt) * -1.0
t2pOffset = maxTideFt * t2pFactor * -1.0
print("t2pFactor", t2pFactor)
print("t2pOffset", t2pOffset)
def tideToPix(t):
    # return (14.0 - t * -1) * 10 - 130
    return (t) * t2pFactor + t2pOffset
    # return int(t * -8.57142857143 + 106.857142857 + 64.0)
    # return (((14.0 - t * -1) * 10 - 130) - 128) * -1 + 64 + 10
    # return (((14.0 - float(t) * -1.0) * 10.0 - 130.0) - float(magtag.graphics.display.height)) * -1.0 + 64.0
    # rv = (14.0 - t * -1) * 10 - 130
    # print (t, "tideToPix", rv)
    #return rv

print("tideToPix(12.0)", tideToPix(12.0))
print("tideToPix(-2.0)", tideToPix(-2.0))

dir = 0
startX = 0
startY = 0
for dispD in filter(tideFilter, tideData):
    endX = dayToPix(dispD[0])
    endY = tideToPix(dispD[4])
    # print(dir)
    if not dir == 0:
        tidal(int(startX), int(startY), int(endX), int(endY), dir)
    dir = 1
    if dispD[6] == "H":
        dir = -1
    startX = dayToPix(dispD[0])
    startY = tideToPix(dispD[4])


# testPos = magtag.add_text(
#     text_position=(
#         148,
#         (magtag.graphics.display.height // 2) - 1,
#     ),
#     text_scale=1,
# )
# magtag.set_text("08/02", textPos)

time.sleep(3.5)
magtag.graphics.display.refresh()

while True:
    time.sleep(2.5)
