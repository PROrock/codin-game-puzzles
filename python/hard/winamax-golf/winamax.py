import copy

import sys

HOLE = 'H'
FILLED_HOLE = 'F'
WATER = 'X'
DOT = '.'
ARROWS = list("<>^v")
FORBIDDEN = set([WATER, FILLED_HOLE, *ARROWS])

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
    if(not is_inbounds(point)):
        return WATER
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
    def __init__(self, p, dist, path, course):
        self.p = p
        self.dist = dist
        self.path = path
        self.course = course
    def __repr__(self):
        # todo path maybe?
        return f"N({self.p}, dist={self.dist})"

    def set_arrow(self, course, poss_dir, arrow):
        p = self.p
        for _ in range(self.dist):
            set_mapping(course, p, arrow)
            p = p.add(poss_dir)

    def expand(self):
        if(self.dist == 0):
            return []

        new_nodes = []
        # possibilities = [Point(x,y) for x,y in zip([-1,1,0,0],[0,0,-1,1])]
        # debug(f"expand {self}")
        # random.shuffle(possibilities) # maybe worse than without shuffle?
        for poss, arrow in possibilities2:
            mult_poss = poss.mult(self.dist)
            new_p = self.p.add(mult_poss)

            if not is_inbounds(new_p):
                continue

            map_value = mapping(grid, new_p)
            # debug(f"new_point is {new_p}, map_val is: {map_value}, poss={poss}, arr={arrow}")
            if map_value in [DOT, HOLE]:
                new_course = copy.deepcopy(self.course)
                self.set_arrow(new_course, poss, arrow)
                # debug(f"GOOD new_point is {new_p}, map_val is: {map_value}, poss={poss}, arr={arrow}")
                print_grid(new_course)
                new_nodes.append(Node(new_p, self.dist-1, copy.copy(self.path)+[self.p], copy.deepcopy(new_course)))
        # debug(f"expanded from {self} are: {[str(node) for node in new_nodes]}")
        return new_nodes

class Search:
    def __init__(self, start, course):
        self.start = start
        self.course = course

    def search(self):
        front = [Node(self.start, int(mapping(grid, self.start)), [], self.course)]

        while len(front) > 0:
            node = front.pop(0) ## take first element -> breadth-first
            if mapping(node.course, node.p) == HOLE:
                node.path.append(node.p)
                set_mapping(node.course, node.p, FILLED_HOLE)
                debug(f"Found goal: '{mapping(grid, node.p)}'. Dist {node.dist}. Path is {node.path}")
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

def find_ball(grid):
    for y in range(height):
        for x in range(width):
            # todo - can be faster if no point
            value = mapping(grid, Point(x,y))
            if value in list("123456789"):
                return x, y, value
    return None

# def is_valid(course, ):

def solve(course):
    curr_course = course
    while True:
        # for one ball
        ball = find_ball(curr_course)
        if ball is None:
            break

        x, y, value = ball
        # print(x, y, value)
        final_node = Search(Point(x,y), curr_course).search()
        debug(f"")


        curr_course = final_node.course
        print_grid(curr_course)

    return final_node.course

result = solve(grid)
for row in result:
    replaced = [c.replace(FILLED_HOLE, DOT).replace(WATER, DOT) for c in row]
    print(''.join(replaced))
