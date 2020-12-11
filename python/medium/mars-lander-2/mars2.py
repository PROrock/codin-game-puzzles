import math
import sys

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

G = 3.711  # m/s^2
HEIGHT = 3000  # m
WIDTH = 7000  # m
DELTA_T = 1  # second
P_MIN = 0
P_MAX = 4
P_MAX_STEP = 1
# A_MIN = -90
# A_MAX = 90
A_MIN = -25
A_MAX = 25
A_MAX_STEP = 15

sign = lambda x: 0 if x==0 else int(math.copysign(1,x))


class Lander:
    def __init__(self, x, y, hSpeed, vSpeed, fuel, rotate, power):
        self.x = x
        self.y = y
        self.hSpeed = hSpeed
        self.vSpeed = vSpeed
        self.fuel = fuel
        self.rotate = rotate
        self.power = power


def debug(s):
    print(s, file=sys.stderr, flush=True)


def readSurface():
    # the number of points used to draw the surface of Mars.
    surfaceN = int(input())
    surface = []
    for i in range(surfaceN):
        # landX: X coordinate of a surface point. (0 to 6999)
        # landY: Y coordinate of a surface point. By linking all the points together in a sequential fashion, you form the surface of Mars.
        # landX, landY = [int(j) for j in input().split()]
        surface.append([int(j) for j in input().split()])
    return surface


def findLanding(surface):
    last = [None, None]
    for land in surface:
        if(land[1] == last[1]):
            return last, land
        last = land


def getGoalPoint(last, land):
    return [int(math.floor((last[0]+land[0])/2)), last[1]]


def addToPower(p, increment):
    return min(P_MAX, max(P_MIN, p+increment))


def addToAngle(angle, increment):
    return min(A_MAX, max(A_MIN, angle+increment))


def getAngle(lander, goalPoint):
    # if(lander.angle != 0):
    #     return 0;
    diff = goalPoint[0]-lander.x
    return sign(-diff) * min(abs(diff), A_MAX_STEP)


# surface
surface = readSurface()
last, land = findLanding(surface)
# debug(last)
# debug(land)
goalPoint = getGoalPoint(last, land)
debug(goalPoint)

# game loop
while 1:
    # hSpeed: the horizontal speed (in m/s), can be negative.
    # vSpeed: the vertical speed (in m/s), can be negative.
    # fuel: the quantity of remaining fuel in liters.
    # rotate: the rotation angle in degrees (-90 to 90).
    # power: the thrust power (0 to 4).
    X, Y, hSpeed, vSpeed, fuel, rotate, power = [int(i) for i in input().split()]
    lander = Lander(X, Y, hSpeed, vSpeed, fuel, rotate, power)

    angle = addToAngle(lander.rotate, getAngle(lander, goalPoint))

    if vSpeed <= (-40) or angle != 0:
        newPower = addToPower(power, +1)
    else:
        newPower = addToPower(power, -1)

    # rotate power. rotate is the desired rotation angle. power is the desired thrust power.
    print("{} {}".format(angle, newPower))
