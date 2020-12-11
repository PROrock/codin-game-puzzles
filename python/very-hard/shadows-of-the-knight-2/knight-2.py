__author__ = 'ojelinek'
import sys
from math import floor, ceil, log2

def debug(*objs):
    print("DEBUG: ", *objs, file=sys.stderr)


class NumberGuesser:
    def __init__(self, upper_bound, lower_bound=0):
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound

    def guess(self):
        return int(floor((self.lower_bound + self.upper_bound) / 2))

    def updateBounds(self, lastGuess, answer):
        if answer == 0:  # answer == guess:
            debug("Solution found: {}".format(lastGuess))
            self.lower_bound = lastGuess
            self.upper_bound = lastGuess

        # cheating detection
        if self.lower_bound > self.upper_bound:
            raise AssertionError("You are cheating! (Or I am dumb)")

        if answer < 0:  # answer < guess:
            self.upper_bound = lastGuess
        else:  # answer > guess
            self.lower_bound = lastGuess


# 0...5 (6) (012 345)
# my number is 2
# you guess

# log2(10) = 3.xx ?
def ORIG_solveByHalving(self):
    lower_bound = 1
    upper_bound = 10
    answer = None
    debug("I will guess it in max {} turns", ceil(log2(upper_bound - lower_bound + 1)))

    while not answer == 0:
        guess = int(floor((lower_bound + upper_bound) / 2))
        answer = 0  # TODO getNewAnswer(guess)
        if answer == 0:  # answer == guess:
            # sol found!
            return guess

        # cheating detection
        if lower_bound > upper_bound:
            raise AssertionError("You are cheating! (Or I am dumb)")

        lower_bound = guess
        if answer < 0:  # answer < guess:
            upper_bound = guess
        else:  # answer > guess
            pass


def getXGuess(xGuess, bomb_direction):
    if 'L' in bomb_direction:
        answer = -1
    elif 'R' in bomb_direction:
        answer = 1
    else:
        answer = 0
    xGuesser.updateBounds(xGuess, answer)
    return xGuesser.guess()


def getYGuess(yGuess, bomb_direction):
    if 'U' in bomb_direction:
        answer = -1
    elif 'D' in bomb_direction:
        answer = 1
    else:
        answer = 0
    yGuesser.updateBounds(yGuess, answer)
    return yGuesser.guess()

# W: width of the building.
# H: height of the building.
W, H = [int(i) for i in input().split()]
N = int(input()) # maximum number of turns before game over.
X0, Y0 = [int(i) for i in input().split()]

debug("I will guess it in max {} turns".format(ceil(log2(max(W,H) - 0 + 1))))

xGuesser = NumberGuesser(W)
xGuess = X0
yGuesser = NumberGuesser(H)
yGuess = Y0

# game loop
while 1:
    bomb_direction = input() # the direction of the bombs from batman's current location (U, UR, R, DR, D, DL, L or UL)

    xGuess = getXGuess(xGuess, bomb_direction)
    yGuess = getYGuess(yGuess, bomb_direction)
    print(str(xGuess) + " " + str(yGuess)) # the location of the next window Batman should jump to.