import copy
from collections import deque

import sys

HOLE = '0'

def debug(text):
    print(text, file=sys.stderr,flush=True)

class Point:
    """Immutable 2D point"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def l1dist(self, other_point):
        d = abs(self.x-other_point.x) + abs(self.y-other_point.y)
        # print(f"l1 dist: {self} and {other_point} is {d}", file=sys.stderr, flush=True)
        return Ld

    def __repr__(self):
        return f"P({self.x},{self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __add__(self, other_point):
        return Point((self.x + other_point.x), (self.y+other_point.y))
    def __mul__(self, multiplier):
        return Point(self.x * multiplier, self.y * multiplier)

class State:
    def __init__(self, bikes, v):
        self.bikes=bikes
        self.v=v # speed
    def __repr__(self) -> str:
        return f"S:{self.bikes}, v={self.v}"
    def __eq__(self, other):
        return self.bikes==other.bikes and self.v==other.v
    def __hash__(self):
        return hash((tuple(self.bikes), self.v))
    # def valid(self):
    #     if 0 > self.v >= 50:
    #         return False
    #     for b in self.bikes:
    #         if grid[b.y][b.x]==False:
    #             return False
    #     return True

def valid_speed(speed):
    return 0 < speed < 50

def validMove(bikes, speed):
    for s in range(speed):
        for b in bikes:
            if b.x+s+1 < length and grid[b.y][b.x+s+1]==False:
                return False
    return True

def validMoveY(bikes, speed, y):
    # if 0>y>3:
    #     return False
    if any([b.y+y<0 or b.y+y>3 for b in bikes]):
        return False
    for b in bikes:
        for s in range(1,speed):
            if b.x+s < length and (grid[b.y][b.x+s]==False or grid[b.y+y][b.x+s]==False):
                return False
        if b.x+speed < length and grid[b.y+y][b.x+speed]==False:
            return False

    return True

def validJump(bikes, speed):
    for b in bikes:
        if b.x+speed < length and grid[b.y][b.x+speed]==False:
            return False
    return True

class Node:
    def __init__(self, state, history=[]):
        self.state=state
        self.history=history
    def __repr__(self):
        return f"N:{self.state}, hist={self.history}"
    def expand(self):
        result = []
        bikes = self.state.bikes
        # SPEED
        x_speed = self.state.v + 1
        if valid_speed(x_speed) and validMove(bikes, x_speed):
            next_bikes = [b + Point(x_speed, 0) for b in bikes]
            result.append(Node(State(next_bikes, x_speed), copy.copy(self.history) + ["SPEED"]))

        # SLOW
        x_speed = self.state.v - 1
        if valid_speed(x_speed) and validMove(bikes, x_speed):
            next_bikes = [b + Point(x_speed, 0) for b in bikes]
            result.append(Node(State(next_bikes, x_speed), copy.copy(self.history) + ["SLOW"]))

        # WAIT
        x_speed = self.state.v
        if valid_speed(x_speed) and validMove(bikes, x_speed):
            next_bikes = [b + Point(x_speed, 0) for b in bikes]
            result.append(Node(State(next_bikes, x_speed), copy.copy(self.history) + ["WAIT"]))

        #JUMP
        x_speed = self.state.v
        if validJump(bikes, x_speed):
            next_bikes = [b + Point(x_speed, 0) for b in bikes]
            result.append(Node(State(next_bikes, x_speed), copy.copy(self.history) + ["JUMP"]))

        # UP
        x_speed = self.state.v
        y=-1
        if validMoveY(bikes, x_speed, y):
            next_bikes = [b + Point(x_speed, y) for b in bikes]
            result.append(Node(State(next_bikes, x_speed), copy.copy(self.history) + ["UP"]))

        # DOWN
        x_speed = self.state.v
        y=1
        if validMoveY(bikes, x_speed, y):
            next_bikes = [b + Point(x_speed, y) for b in bikes]
            result.append(Node(State(next_bikes, x_speed), copy.copy(self.history) + ["DOWN"]))


        # debug(f"Expanded {self} to {result}")
        return result

def search(bikes, speed):
    visited=set()
    q=deque([Node(State(bikes, speed))])
    while q:
        node = q.popleft()
        if node.state in visited:
            continue

        if node.state.bikes[0].x >= length:
            debug(f"Found solution: {node}")
            return node
        expanded = node.expand()
        q.extend(expanded)
        visited.add(node.state)

    debug("Solution not found")
    return None


m = int(input())  # the amount of motorbikes to control
v = int(input())  # the minimum amount of motorbikes that must survive
debug(m)
debug(v)
# l0 = input()  # L0 to L3 are lanes of the road. A dot character . represents a safe space, a zero 0 represents a hole in the road.
# l1 = input()
# l2 = input()
# l3 = input()
# debug(l0)
# debug(l1)
# debug(l2)
# debug(l3)
grid = [[c!=HOLE for c in input()] for _ in range(4)]
length = len(grid[0])
# for g in grid:
#     debug(g)

# game loop
while True:
    bikes=[]
    s = int(input())  # the motorbikes' speed
    for i in range(m):
        # x: x coordinate of the motorbike
        # y: y coordinate of the motorbike
        # a: indicates whether the motorbike is activated "1" or destroyed "0"
        x, y, a = [int(j) for j in input().split()]
        debug(f"{(x,y,a)}")
        if a:
            bikes.append(Point(x,y))

    node = search(bikes, s)
    # A single line containing one of 6 keywords: SPEED, SLOW, JUMP, WAIT, UP, DOWN.
    print(node.history[0] if node and node.history else "SPEED")
