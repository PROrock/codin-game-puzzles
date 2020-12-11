import math
import sys

G = 3.711  # m/s^2
HEIGHT = 3000  # m
WIDTH = 7000  # m
DELTA_T = 1  # second
P_MIN = 0
P_MAX = 4  # m/s^2
P_MAX_STEP = 1
# A_MIN = -90
# A_MAX = 90
A_MIN = -45
A_MAX = 45
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
    return min(P_MAX, max(2, p+increment))

def addToAngle(angle, increment, goal_y, lander_y, vSpeed):
    coef = get_coeff_max_angle(goal_y, lander_y, vSpeed)
    debug(f"goal_y - lander_y={goal_y - lander_y}, m*vSpeed={30*vSpeed}, coeff is {coef}")
    return int(min(coef*A_MAX, max(coef*A_MIN, angle+increment)))


def get_coeff_max_angle(goal_y, lander_y, vSpeed):
    return 0.2 if goal_y - lander_y > 40 * vSpeed else 1


def get_x_speed(angle, thrust):
    return thrust * math.sin(angle)

def get_angle_increment(lander, goalPoint, hSpeed, vSpeed, last, land):
    if last[0] <= lander.x <= land[0] and abs(hSpeed) <= 2:
        diff_angle = -lander.rotate
        debug(f"Over ")
        return sign(diff_angle) * min(abs(diff_angle), A_MAX_STEP)

    coeff = get_coeff_max_angle(last[1], lander.y, vSpeed)

    dir_to_goal = goalPoint[0] - lander.x
    n_turns = abs(dir_to_goal) // max(abs(hSpeed), 1)
    brake_speed = get_x_speed(coeff*A_MAX, P_MAX)
    brake_turns = abs(hSpeed) / abs(brake_speed)
    angle_diff_abs = abs(sign(dir_to_goal) * coeff*A_MAX - lander.rotate)
    angle_brake_turns = angle_diff_abs / A_MAX_STEP
    braking_turns = math.ceil(brake_turns + angle_brake_turns)
    debug(f"brake_turns={brake_turns}, angle_diff_abs={angle_diff_abs}, angle_brake_turns={angle_brake_turns}; N turns={n_turns}")
    if braking_turns >= n_turns:
        # brake
        debug(f"Braking")
        return sign(hSpeed) * min(angle_diff_abs, A_MAX_STEP)

    diff = goalPoint[0]-lander.x-15*hSpeed
    debug(f"diff={diff}")
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

    angle_increment = get_angle_increment(lander, goalPoint, hSpeed, vSpeed, last, land)
    angle = addToAngle(lander.rotate, angle_increment, last[1], lander.y, vSpeed)

    if vSpeed <= (-40) or angle != 0:
        newPower = addToPower(power, +1)
    else:
        newPower = addToPower(power, -1)

    debug(f"Lander rotate={lander.rotate}, angle_incr={angle_increment}")
    # rotate power. rotate is the desired rotation angle. power is the desired thrust power.
    print("{} {}".format(angle, newPower))
