import copy

import sys

MAX_DEPTH = 30
HOLE = 'H'
FILLED_HOLE = 'F'
WATER = 'X'
DOT = '.'
ARROWS = list("<>^v")
# FORBIDDEN = set([WATER, FILLED_HOLE, *ARROWS])
NUMBERS = set("123456789")

grid = []

def debug(text):
    print(text, file=sys.stderr,flush=True)

def print_grid(grid):
    for row in grid:
        debug(row)
    debug(' ')

def is_inbounds(point):
    return not (point.x < 0 or point.x >= width or point.y < 0 or point.y >= height)

def mapping(grid, point):
    # if(not is_inbounds(point)):
    #     return WATER
    return grid[point.y][point.x]

def set_mapping(grid, point, value):
    grid[point.y][point.x] = value


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
    def mult(self, multiplier):
        return Point(self.x * multiplier, self.y * multiplier)


class Node:
    def __init__(self, dist, course):
        self.dist = dist
        self.course = course
    def __repr__(self):
        return f"N(dist={self.dist})"

    def set_arrow(self, course, p, poss_dir, arrow, dist):
        for _ in range(dist):
            set_mapping(course, p, arrow)
            p = p.add(poss_dir)
        set_mapping(course, p, str(dist-1))

    def get_final_p(self, p, poss, dist):
        new_p = p
        for _ in range(dist-1):
            new_p = new_p.add(poss)
            if not is_inbounds(new_p) or not mapping(self.course, new_p) in set([DOT, WATER]):
                return None

        new_p = new_p.add(poss)
        if not is_inbounds(new_p) or not mapping(self.course, new_p) in [DOT, HOLE]:
            return None
        if dist==1 and mapping(self.course, new_p) != HOLE:
            return None
        return new_p

    def expand(self):
        # ball = find_ball(self.course)
        ball = highest_ball(self.course)
        if ball is None:
            return []

        x,y,dist = ball
        dist = int(dist)
        p = Point(x,y)

        new_nodes = []
        debug(f"expand {self}")
        for poss, arrow in possibilities2:
            new_p = self.get_final_p(p, poss, dist)
            if new_p is None:
                continue

            # debug(f"new_point is {new_p}, map_val is: {mapping(grid, new_p)}, poss={poss}, arr={arrow}")
            new_course = copy.deepcopy(self.course)
            self.set_arrow(new_course, p, poss, arrow, dist)
            # debug(f"GOOD new_point is {new_p}, map_val is: {map_value}, poss={poss}, arr={arrow}")
            print_grid(new_course)
            new_nodes.append(Node(self.dist+1, copy.deepcopy(new_course)))
        # debug(f"expanded from {self} are: {[str(node) for node in new_nodes]}")
        return new_nodes

class Search:
    def __init__(self, start, course):
        self.start = start
        self.course = course

    def search(self):
        front = [Node(0, self.course)]

        while len(front) > 0:
            node = front.pop(0) ## take first element -> breadth-first
            # if node.dist >= MAX_DEPTH:
            #     debug(f"Node.dist exceeded ({node.dist}). Terminating.")
            #     return None

            if find_ball(node.course) is None:
                debug(f"Found goal. Dist {node.dist}.")
                return node
            new_nodes = node.expand()
            front.extend(new_nodes)
        debug(f"Haven't found one of goals(H) for start: {self.start}")
        return None


possibilities2 = [(Point(x,y),arr) for x,y,arr in zip([-1,1,0,0],[0,0,-1,1],list("<>^v"))]

width, height = [int(i) for i in input().split()]
for i in range(height):
    row = list(input())
    grid.append(row)

print_grid(grid)

def find_ball(course):
    for y in range(height):
        for x in range(width):
            value = course[y][x]
            if value in NUMBERS and grid[y][x] != HOLE:
                return x, y, value
    return None

def highest_ball(course):
    max_val = -1
    max_xy = (None, None)
    for y in range(height):
        for x, value in enumerate(course[y]):
            if value in NUMBERS and int(value) > max_val and grid[y][x] != HOLE:
                max_val = int(value)
                max_xy = (x,y)
    return (*max_xy, max_val)


def solve(course):
    final_node = Search(None, course).search()
    debug("")
    return final_node.course

result = solve(grid)
for row in result:
    replaced = [DOT if c in set("0123456789FX") else c for c in row]
    print(''.join(replaced))
