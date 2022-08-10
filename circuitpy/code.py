import math
import time
import json
tideData = []
dayNumber = 216.0
date0String = ""
dateLString = ""
zoomDays = 4
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

def tideFilter(e):
    return e[0] >= (dayNumber - 0.3) and e[0] < (dayNumber + zoomDays + 0.3)

def displayAll():
    global date0String, dayNumber, zoomDays
    date0String = ""
    # Make a background color fill
    color_bitmap = displayio.Bitmap(magtag.graphics.display.width, magtag.graphics.display.height, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0xFFFFFF
    bg_sprite = displayio.TileGrid(color_bitmap, x=0, y=0, pixel_shader=color_palette)
    magtag.graphics.splash.append(bg_sprite)
    ##########################################################################
    # night time, day time
    startX = 0
    endX = 0
    for e in filter(sunFilter, sunData):
        if e[3] == "R": # R == Rise, the end of night
            endX = dayToPix(e[0])
            if zoomDays <= 14:
                dateLoc = magtag.add_text(
                    text_position=(
                        int(dayToPix(e[0])),
                        122,
                    ),
                    text_scale=1,
                )
                dateTxt = e[4]
                if zoomDays > 3:
                    dateTxt = e[4].split(' ')[0]
                if zoomDays > 7:
                    dateTxt = e[4].split(' ')[2]
                magtag.set_text(dateTxt, dateLoc, False)
            if date0String == "":
                date0String = e[4]
        if e[3] == "S":
            startX = dayToPix(e[0])
        if not endX == 0 and e[3] == "R":
            print("night rectangle", int(startX), 0, int(endX-startX), magtag.graphics.display.height)
            magtag.graphics.splash.append(Rect(int(startX), 0, int(endX-startX), magtag.graphics.display.height, fill=0x999999, outline=0x999999))

    # # rising and falling tides
    maxTideFt = 11.5
    minTideFt = -1.7
    t2pFactor = magtag.graphics.display.height / (maxTideFt - minTideFt) * -1.0
    t2pOffset = maxTideFt * t2pFactor * -1.0
    print("t2pFactor", t2pFactor)
    print("t2pOffset", t2pOffset)
    def tideToPix(t):
        return (t) * t2pFactor + t2pOffset

    dir = 0
    startX = 0
    startY = 0
    for dispD in filter(tideFilter, tideData):
        endX = dayToPix(dispD[0])
        endY = tideToPix(dispD[4])
        if not dir == 0:
            tidal(int(startX), int(startY), int(endX), int(endY), dir)
        dir = 1
        if dispD[6] == "H":
            dir = -1
        startX = dayToPix(dispD[0])
        startY = tideToPix(dispD[4])

    date0Txt = magtag.add_text(
        text_position=(
            1,
            7,
        ),
        text_scale=1,
    )
    magtag.set_text(date0String, date0Txt, True)
    #     time.sleep(3.5)
    #     magtag.graphics.display.refresh()


lastButtonTime = time.monotonic()
displayAll()
while True:
    time.sleep(0.05)
    if lastButtonTime + 10.0 < time.monotonic():
        magtag.peripherals.neopixel_disable = False
        magtag.peripherals.neopixels.fill((25, 25, 25))
        time.sleep(0.5)
        magtag.peripherals.neopixels.fill((0, 0, 0))
        time.sleep(0.5)
        magtag.peripherals.neopixels.fill((250, 250, 250))
        time.sleep(0.5)
        magtag.peripherals.neopixel_disable = False
        #sleep for a day
        magtag.exit_and_deep_sleep(24 * 60 * 60) # one day
    magtag.peripherals.neopixel_disable = True
    # buttons 0-3 pressed (== 0 volts)
    if magtag.peripherals.buttons[0].value == 0:
        lastButtonTime = time.monotonic()
        dayNumber = dayNumber - zoomDays
        if dayNumber < 1:
            dayNumber = 1.0
        magtag.peripherals.neopixel_disable = False
        magtag.peripherals.neopixels.fill((25, 25, 0))
        displayAll()
    if magtag.peripherals.buttons[1].value == 0:
        lastButtonTime = time.monotonic()
        zoomDays /= 2
        if zoomDays < 1:
            zoomDays = 1
        magtag.peripherals.neopixel_disable = False
        magtag.peripherals.neopixels.fill((0, 25, 0))
        displayAll()
    if magtag.peripherals.buttons[2].value == 0:
        lastButtonTime = time.monotonic()
        zoomDays *= 2
        if zoomDays > 32:
            zoomDays = 32
        magtag.peripherals.neopixel_disable = False
        magtag.peripherals.neopixels.fill((25, 0, 0))
        displayAll()
    if magtag.peripherals.buttons[3].value == 0:
        lastButtonTime = time.monotonic()
        dayNumber = dayNumber + zoomDays
        if dayNumber > 365 - zoomDays:
            dayNumber = 365 - zoomDays
        magtag.peripherals.neopixel_disable = False
        magtag.peripherals.neopixels.fill((0, 25, 25))
        displayAll()
