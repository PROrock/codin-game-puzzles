import bisect
import copy

import sys

HOLE = 'H'
FILLED_HOLE = 'F'
WATER = 'X'
DOT = '.'
ARROWS = list("<>^v")
NUMBERS = set("123456789")
LAND_VALID_CHARS = set([DOT, HOLE])
FLIGHT_VALID_CHARS = set([DOT, WATER])
DIST_0_LAND_VALID_CHARS = {HOLE}


PRINT_DEBUG = False
global_dist = 0

grid = []

def debug(text):
    if PRINT_DEBUG:
        print(text, file=sys.stderr,flush=True)

def print_grid(grid):
    for row in grid:
        debug(row)
    debug(' ')

def is_inbounds(point):
    return not (point.x < 0 or point.x >= width or point.y < 0 or point.y >= height)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"P({self.x},{self.y})"
    def __eq__(self, othr):
        return (self.x, self.y) ==(othr.x, othr.y)
    def __hash__(self):
        return hash((self.x, self.y))
    def add(self, other_point):
        return Point(self.x + other_point.x, self.y+other_point.y)

class Ball:
    def __init__(self, p, dist):
        self.p=p
        self.dist=dist
    def __lt__(self, other):
        # reverse order! Min dist is at the end!
        # reason - find out that there is no HOLE in neighborhood of a 1-ball soon
        return self.dist > other.dist
    def __repr__(self):
        return f"B({self.p}, {self.dist})"
    def __eq__(self, other):
        return self.p.x==other.p.x and self.p.y==other.p.y # and self.dist==other.dist

class Node:
    def __init__(self, dist, course, balls):
        self.dist = dist
        self.course = course
        self.balls = balls
    def __repr__(self):
        return f"N(dist={self.dist})"

    def set_arrow(self, course, p, poss_dir, arrow, dist):
        for _ in range(dist):
            course[p.y][p.x] = arrow
            p = p.add(poss_dir)
        course[p.y][p.x] = str(dist - 1)

    def backtrack_arrow(self, course, p, poss_dir, dist):
        course[p.y][p.x] = str(dist)
        for _ in range(dist):
            p = p.add(poss_dir)
            course[p.y][p.x] = grid[p.y][p.x]

    def get_final_p(self, p, poss, dist):
        new_p = p
        for _ in range(dist-1):
            new_p = new_p.add(poss)
            if not is_inbounds(new_p) or not self.course[new_p.y][new_p.x] in FLIGHT_VALID_CHARS:
                return None

        new_p = new_p.add(poss)
        land_valid_chars = LAND_VALID_CHARS if dist > 1 else DIST_0_LAND_VALID_CHARS
        if not is_inbounds(new_p) or not self.course[new_p.y][new_p.x] in land_valid_chars:
            return None
        return new_p

    def recur(self):
        # debug(f"recur {self}: balls={balls}")
        global global_dist
        # if global_dist >= 50000:
        #     return 1

        processed_balls = []
        ball=None
        while ball is None:
            if not balls:
                return self
            ball = balls.pop()
            # debug(f"ball={ball}")
            p, dist = ball.p, ball.dist
            if dist == 0 or grid[p.y][p.x] == HOLE: # -> don't expand it more
                processed_balls.append(ball)
                ball = None
        processed_balls.append(ball)

        # print_grid(self.course)
        for poss, arrow in possibilities2:
            new_p = self.get_final_p(p, poss, dist)
            if new_p is None:
                continue

            new_course = self.course
            self.set_arrow(new_course, p, poss, arrow, dist)
            new_ball = Ball(new_p, dist - 1)
            bisect.insort(balls, new_ball)
            global_dist += 1
            result = Node(global_dist, new_course, balls).recur()
            if result:
                return result
            # debug(f"Backtracking from {new_ball}")
            self.backtrack_arrow(new_course, p, poss, dist)
            balls.remove(new_ball)

        # debug(f"Cannot move ball {ball}, returning processed_balls {processed_balls}, back to balls")
        balls.extend(processed_balls[::-1])
        return None


possibilities2 = [(Point(x,y),arr) for x,y,arr in zip([-1,1,0,0],[0,0,-1,1],list("<>^v"))]

width, height = [int(i) for i in input().split()]
for i in range(height):
    row = list(input())
    grid.append(row)

# print_grid(grid)

def get_balls(course):
    balls=[]
    for y in range(height):
        for x, value in enumerate(course[y]):
            if value in NUMBERS:
                balls.append(Ball(Point(x, y), int(value)))
    return balls

course = copy.deepcopy(grid)
balls = get_balls(course)
balls.sort()

result_node = Node(0, course, balls).recur()
result = result_node.course
for row in result:
    replaced = [DOT if c in set("0123456789FX") else c for c in row]
    print(''.join(replaced))
