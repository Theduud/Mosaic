import cairo
import math
import random
import numpy as np
import sys
from PIL import Image
import os

img = Image.open("input.png").convert('RGB')
pixels = img.load()

WIDTH = img.width
HEIGHT = img.height
s = cairo.SVGSurface("surface.svg", WIDTH, HEIGHT)
c = cairo.Context(s)


def FormatColors(colorsHex):
    newArray = []
    for color in colorsHex:
        color = tuple(int(color[i: i + 2], 16) for i in (0, 2, 4))
        newArray.append([color[0] / 255, color[1] / 255, color[2] / 255])
    return newArray


def SetRGB(color, a=1):
    c.set_source_rgba(color[0], color[1], color[2], a)


def Clear():
    c.save()
    SetRGB(bgColor)
    c.paint()
    c.restore()


class Point:
    def __init__(self, x, y, color=[0, 0, 0]):
        self.x = x
        self.y = y
        self.color = color

    def GetDistance(self, point):
        return abs(math.sqrt(((self.x - point.x)**2)+((self.y - point.y)**2)))


colors = FormatColors(["f72585", "b5179e", "7209b7", "560bad",
                       "480ca8", "3a0ca3", "3f37c9", "4361ee", "4895ef", "4cc9f0"])
bgColor = [0, 0, 0]
Clear()
numPoints = 50
points = []
colorInt = 0
for i in range(numPoints):
    x = random.randint(0, WIDTH - 1)
    y = random.randint(0, HEIGHT - 1)
    color = [pixels[x, y][0]/255, pixels[x, y][1]/255, pixels[x, y][2]/255]
    points.append(Point(x, y, color))
    colorInt += 1
    if colorInt >= len(colors):
        colorInt = 0
for x in range(WIDTH):
    for y in range(HEIGHT):
        closePoint = points[0]
        absD = 100
        for point in points:
            p = Point(x, y)
            d1 = p.GetDistance(point)
            d2 = p.GetDistance(closePoint)
            if d1 != d2:
                if d1 - d2 < absD:
                    absD = abs(d1-d2)
                if d1 < d2:
                    closePoint = point
        SetRGB(closePoint.color)
        if absD <= 2:
            SetRGB([0, 0, 0])
        c.rectangle(x, y, 1, 1)
        c.fill()
SetRGB([1, 1, 1])
# for point in points:
#     c.arc(point.x, point.y, 5, 0, math.pi * 2)
#     c.fill()
s.write_to_png("output1.png")
