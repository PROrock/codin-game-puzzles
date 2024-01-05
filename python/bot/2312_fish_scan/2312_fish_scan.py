import sys
import math
from dataclasses import dataclass
from typing import NamedTuple, Optional


def debug(*s):
    print(*s, file=sys.stderr, flush=True)


class Vect(NamedTuple):
    """Immutable 2D vector"""
    x: int
    y: int

    # def __init__(self, x, y):
    #     self.x = x
    #     self.y = y

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

    def normalize(self):
        """Normalize vector to be able to compare it with other vectors (possibly multiplies of this one)"""
        gcd_xy = math.gcd(self.x, self.y)
        if gcd_xy == 0 or gcd_xy == 1:
            return self
        return Vect(self.x / gcd_xy, self.y / gcd_xy)

    # this doesn't work as len must return integer not float!
    # def __len__(self):
    #     return math.sqrt(self.x**2 + self.y**2)

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


@dataclass
class Drone:
    id: int
    coor: Vect
    emergency: str
    battery: int


@dataclass
class Creature:
    id: int
    coor: Optional[Vect]
    velocity: Optional[Vect]
    color: int
    type_: int


# Score points by scanning valuable fish faster than your opponent.

creatures = {}
creature_count = int(input())
for i in range(creature_count):
    creature_id, color, _type = [int(j) for j in input().split()]
    creatures[creature_id] = Creature(creature_id, None, None, color, _type)

scanned_creatures_ids = set()

# game loop
while True:
    my_score = int(input())
    foe_score = int(input())

    my_nearby_creatures = []
    my_scan_count = int(input())
    for i in range(my_scan_count):
        creature_id = int(input())
        my_nearby_creatures.append(creatures[creature_id])

    foe_scan_count = int(input())
    for i in range(foe_scan_count):
        creature_id = int(input())

    my_drones = {}
    my_drone_count = int(input())
    for i in range(my_drone_count):
        drone_id, drone_x, drone_y, emergency, battery = [int(j) for j in input().split()]
        my_drones[drone_id] = Drone(drone_id, Vect(drone_x, drone_y), emergency, battery)
    foe_drone_count = int(input())
    for i in range(foe_drone_count):
        drone_id, drone_x, drone_y, emergency, battery = [int(j) for j in input().split()]

    drone_scan_count = int(input())
    for i in range(drone_scan_count):
        drone_id, creature_id = [int(j) for j in input().split()]
        scanned_creatures_ids.add(drone_id)

    # todo here aby coor
    # visible_creature =
    visible_creature_count = int(input())
    for i in range(visible_creature_count):
        creature_id, creature_x, creature_y, creature_vx, creature_vy = [int(j) for j in input().split()]
        creature = creatures[creature_id]
        creature.coor = Vect(creature_x, creature_y)
        creature.velocity = Vect(creature_vx, creature_vy)
    radar_blip_count = int(input())
    for i in range(radar_blip_count):
        inputs = input().split()
        drone_id = int(inputs[0])
        creature_id = int(inputs[1])
        radar = inputs[2]
        # ignore

    for i in range(my_drone_count):
        # set([for creature in creatures if creature.coor is not None])
        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr, flush=True)

        # MOVE <x> <y> <light (1|0)> | WAIT <light (1|0)>
        print("WAIT 1")
