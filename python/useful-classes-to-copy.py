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

    def __add__(self, other_point):
        return Point((self.x + other_point.x), (self.y+other_point.y))
    def __sub__(self, other_point):
        return Point((self.x - other_point.x), (self.y-other_point.y))
    def __mul__(self, multiplier):
        return Point(self.x * multiplier, self.y * multiplier)

class Vect:
    """Immutable 2D vector"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def l1dist(self, other_vect):
        d = abs(self.x-other_vect.x) + abs(self.y-other_vect.y)
        # print(f"l1 dist: {self} and {other_vect} is {d}", file=sys.stderr, flush=True)
        return d

    def l1_norm(self):
        return abs(self.x) + abs(self.y)

    def l2_norm(self):
        return math.sqrt(self.x**2 + self.y**2)

    def l_inf_norm(self):
        return max(abs(self.x), abs(self.y))

    def normalize(self):
        """Normalize vector to be able to compare it with other vectors (possibly multiplies of this one)"""
        gcd_xy = gcd(self.x, self.y)
        if gcd_xy == 0 or gcd_xy == 1:
            return self
        return Vect(self.x / gcd_xy, self.y / gcd_xy)

    # this doesn't work as len must return integer not float!
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
    def __mul__(self, multiplier):
        return Vect(self.x * multiplier, self.y * multiplier)

class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        self.vector = point2 - point1

    def __contains__(self, point):
        t = self._compute_t(point)
        return self._contains(point, t)

    def contains_in_line_segment(self, point):
        t = self._compute_t(point)
        return self._contains(point, t) and 0 < max(t[0], t[1]) < 1

    def _compute_t(self, point):
        return [None if self.vector.x == 0 else (point.x - self.point1.x) / float(self.vector.x),
                None if self.vector.y == 0 else (point.y - self.point1.y) / float(self.vector.y)]

    def _contains(self, point, t):
        return t[0] is None and point.x == self.point1.x \
               or t[1] is None and point.y == self.point1.y \
               or t[0] == t[1]


