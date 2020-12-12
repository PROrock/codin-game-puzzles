__author__ = 'ojelinek'
import sys
from math import floor, ceil, log2

COLDER, WARMER, SAME, UNKNOWN='COLDER', 'WARMER', 'SAME', 'UNKNOWN'

def debug(*objs):
    print("DEBUG: ", *objs, file=sys.stderr, flush=True)

def int_middle(lower_bound, upper_bound):
    return int(floor((lower_bound + upper_bound) / 2))


class NumberGuesser:
    def __init__(self, upper_bound, lower_bound=0):
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound

    # def guess(self):
    #     return int_middle(self.lower_bound, self.upper_bound)

    def updateBounds(self, curr, prev, bomb_dist):
        debug(f"curr bounds: {self.lower_bound}-{self.upper_bound}")
        debug(curr, prev, bomb_dist)

        if bomb_dist == UNKNOWN:
            return self.guess_new(curr)

        middle = int_middle(curr, prev)
        if bomb_dist == SAME:
            debug("Solution found: {}".format(middle))
            self.lower_bound = middle
            self.upper_bound = middle

        dir = curr-prev>0
        debug(f"dir={dir}, bomb_dist == WARMER:{bomb_dist == WARMER}")
        if dir == (bomb_dist == WARMER):
            self.lower_bound = middle
        else:
            self.upper_bound = middle
        debug(f"new bounds: {self.lower_bound}-{self.upper_bound}")

        # cheating detection
        if self.lower_bound > self.upper_bound:
            raise AssertionError("You are cheating! (Or I am dumb)")

        return self.guess_new(curr)

    def guess_new(self, curr):
        dist_to_low = abs(curr - self.lower_bound)
        dist_to_upp = abs(curr - self.upper_bound)
        return self.lower_bound if dist_to_low >= dist_to_upp else self.upper_bound-1


def getXGuess(currx, prevx, bomb_direction):
    # if bomb_direction == UNKNOWN:
    #     return xGuesser.guess()
    # if bomb_direction == COLDER:
    return xGuesser.updateBounds(currx, prevx, bomb_direction)
    # return xGuesser.guess()


def getYGuess(curry, prevy, bomb_direction):
    return yGuesser.updateBounds(curry, prevy, bomb_direction)
    # return yGuesser.guess()

# W: width of the building.
# H: height of the building.
W, H = [int(i) for i in input().split()]
N = int(input()) # maximum number of turns before game over.
X0, Y0 = [int(i) for i in input().split()]  # Batman start position

debug(W, H, N, X0, Y0)
debug("I will guess it in max {} turns".format(ceil(log2(max(W,H) - 0 + 1))))

xGuesser = NumberGuesser(W)
currx = X0
yGuesser = NumberGuesser(H)
curry = Y0

prevx, prevy = X0, Y0
# game loop
while 1:
    bomb_dir = input()  # Current distance to the bomb compared to previous distance (COLDER, WARMER, SAME or UNKNOWN)

    new_currx = getXGuess(currx, prevx, bomb_dir)
    new_curry = getYGuess(curry, prevy, bomb_dir)
    if bomb_dir != UNKNOWN:
        prevx, prevy = currx, curry
    currx, curry = new_currx, new_curry
    print(str(currx) + " " + str(curry)) # the location of the next window Batman should jump to.

