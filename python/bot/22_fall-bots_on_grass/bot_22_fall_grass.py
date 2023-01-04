import dataclasses
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

@dataclasses.dataclass(frozen=True)
class Tile:
    scrap_amount: int
    owner: int
    "# owner: 1 = me, 0 = foe, -1 = neutral"
    units: int
    recycler: bool
    can_build: bool
    can_spawn: bool
    in_range_of_recycler: bool

    def __repr__(self):
        return f"T({self.scrap_amount}, {owner}, {units})"

def debug(*s):
    print(*s, file=sys.stderr, flush=True)

def move(amount: int, from_: Vect, to: Vect):
    return f"MOVE {amount} {from_.x} {from_.y} {to.x} {to.y}"

# def move_old(amount: int, from_x: int, from_y: int, to_x: int, to_y: int):
#     return f"MOVE {amount} {from_x} {from_y} {to_x} {to_y}"

def spawn(amount: int, vect: Vect):
    return f"SPAWN {amount} {vect.x} {vect.y}"

# def spawn_old(amount: int, x: int, y: int):
#     return f"SPAWN {amount} {x} {y}"


width, height = [int(i) for i in input().split()]

while True:
    actions = []
    my_first_spawn_tile = None
    map = []
    my_tiles = []
    my_units = []

    my_matter, opp_matter = [int(i) for i in input().split()]
    for i in range(height):
        map_row = []
        for j in range(width):
            # owner: 1 = me, 0 = foe, -1 = neutral
            scrap_amount, owner, units, recycler, can_build, can_spawn, in_range_of_recycler = [int(k) for k in input().split()]
            tile = Tile(scrap_amount, owner, units, bool(recycler), bool(can_build), bool(can_spawn), bool(in_range_of_recycler))
            map_row.append(tile)
            if my_first_spawn_tile is None and tile.can_spawn:
                my_first_spawn_tile = Vect(j, i)
            if tile.owner == 1:
                my_tiles.append(tile)
                if tile.units:
                    my_units.append((Vect(j, i), tile.units, tile))  # tile.units and tile are duplicate/redundant information

        map.append(map_row)

    # debug(my_matter, opp_matter)
    # debug([(v.x,v.y, units) for v, units, tile in my_units])
    # debug(f"I have {len(my_tiles)} tiles, {len(my_units)} unit tiles, {sum(units for _,_,units,_ in my_units)} units")

    for v, units, tile in my_units:
        target = Vect(random.randrange(0, width), random.randrange(0, height))
        actions.append(move(units, v, target))

    spawn_units = my_matter//10
    if my_first_spawn_tile and spawn_units:
        actions.append(spawn(spawn_units, my_first_spawn_tile))

    print(";".join(actions))
