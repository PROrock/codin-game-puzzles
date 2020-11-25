import math

class Point:
    """Immutable 2D point"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def l1dist(self, other_point):
        d = abs(self.x-other_point.x) + abs(self.y-other_point.y)
        # print(f"l1 dist: {self} and {other_point} is {d}", file=sys.stderr, flush=True)
        return d

    def __repr__(self):
        return f"P({self.x},{self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def add(self, other_point):
        return Point((self.x + other_point.x), (self.y+other_point.y))

class Vect:
    """Immutable 2D vector"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def l1dist(self, other_vect):
        d = abs(self.x-other_vect.x) + abs(self.y-other_vect.y)
        # print(f"l1 dist: {self} and {other_vect} is {d}", file=sys.stderr, flush=True)
        return d

    def __len__(self):
        return math.sqrt(self.x**2 + self.y**2)

    def __repr__(self):
        return f"V({self.x},{self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __add__(self, other):
        return Vect((self.x + other.x), (self.y + other.y))
    def __sub__(self, other):
        return Vect((self.x - other.x), (self.y - other.y))

