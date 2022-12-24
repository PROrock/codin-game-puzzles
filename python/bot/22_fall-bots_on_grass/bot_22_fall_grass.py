import math
import random
import sys

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
        """
        XXX: Consider using math.hypot(*coordinates) or math.dist(p, q), which is probably faster.
        See https://docs.python.org/3/library/math.html#math.dist
        For timing guide, see https://stackoverflow.com/a/24105845/2127340
        """
        return math.sqrt(self.x**2 + self.y**2)

    def l_inf_norm(self):
        return max(abs(self.x), abs(self.y))

    # this doesn't work as len must return integer not float!
    def __len__(self):
        return math.sqrt(self.x**2 + self.y**2)

    def __bool__(self):
        return True

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
    # right multiplication to support 2 * p
    __rmul__ = __mul__
    def __neg__(self):
        return Vect(-self.x, -self.y)
    def round(self, ndigits=None):
        return Vect(round(self.x, ndigits), round(self.y, ndigits))

def debug(*s):
    print(*s, file=sys.stderr, flush=True)

def move(amount: int, from_x: int, from_y: int, to_x: int, to_y: int):
    return f"MOVE {amount} {from_x} {from_y} {to_x} {to_y}"

def spawn(amount: int, x: int, y: int):
    return f"SPAWN {amount} {x} {y}"


width, height = [int(i) for i in input().split()]

while True:
    actions = []
    my_first_spawn_tile = None

    my_matter, opp_matter = [int(i) for i in input().split()]
    for i in range(height):
        for j in range(width):
            # owner: 1 = me, 0 = foe, -1 = neutral
            scrap_amount, owner, units, recycler, can_build, can_spawn, in_range_of_recycler = [int(k) for k in input().split()]
            if my_first_spawn_tile is None and owner == 1 and can_spawn:
                my_first_spawn_tile = Vect(j, i)
            if units and owner == 1:
                actions.append(move(units, j, i, random.randrange(0, width), random.randrange(0, height)))

    spawn_units = my_matter//10
    if my_first_spawn_tile and spawn_units:
        actions.append(spawn(spawn_units, my_first_spawn_tile.x, my_first_spawn_tile.y))

    # print("WAIT")
    print(";".join(actions))
