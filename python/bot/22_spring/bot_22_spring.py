import dataclasses
import math
import sys


def debug(*texts):
    print(texts, file=sys.stderr, flush=True)

# todo create dataclass impl (might be faster?)
# todo consider writing a namedtuple implementation - it enables nice tricks `v[0]` and might be faster
class Point:
    """Immutable 2D point"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def l2_norm(self):
        """
        XXX: Consider using math.hypot(*coordinates) or math.dist(p, q), which is probably faster.
        See https://docs.python.org/3/library/math.html#math.dist
        For timing guide, see https://stackoverflow.com/a/24105845/2127340
        """
        return math.sqrt(self.x**2 + self.y**2)

    def l2_dist(self, other):
        """
        XXX: Consider using math.hypot(*coordinates) or math.dist(p, q), which is probably faster.
        See https://docs.python.org/3/library/math.html#math.dist
        For timing guide, see https://stackoverflow.com/a/24105845/2127340
        """
        return math.hypot(self.x-other.x, self.y-other.y)

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
    # right multiplication to support 2 * p
    __rmul__ = __mul__

@dataclasses.dataclass(frozen=True)
class Entity:
    id: int
    # todo enum?
    type: int
    """type: 0=monster, 1=your hero, 2=opponent hero"""
    p: Point
    shield_life: int
    is_controlled: bool

    @staticmethod
    def create(_id, _type, x, y, shield_life, is_controlled):
        return Entity(_id, _type, Point(x, y), shield_life, bool(is_controlled))

@dataclasses.dataclass(frozen=True)
class Monster(Entity):
    health: int
    vp: Point
    near_base: bool
    threat_for: int

    @staticmethod
    def create(_id, _type, x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for):
        return Monster(_id, _type, Point(x, y), shield_life, bool(is_controlled), health, Point(vx, vy), bool(near_base), threat_for)


def get_nearest_monster(p, monsters):
    min_idx = min(range(len(monsters)), key=lambda i: monsters[i].p.l2_dist(p))
    return monsters[min_idx]


# base_x: The corner of the map representing your base
base_x, base_y = [int(i) for i in input().split()]
base_p = Point(base_x, base_y)
heroes_per_player = int(input())  # Always 3

# game loop
while True:
    entities = []
    for i in range(2):
        # health: Your base health
        # mana: Spend ten mana to cast a spell
        health, mana = [int(j) for j in input().split()]
    entity_count = int(input())  # Amount of heros and monsters you can see
    for i in range(entity_count):
        # _id: Unique identifier
        # _type: 0=monster, 1=your hero, 2=opponent hero
        # x: Position of this entity
        # shield_life: Count down until shield spell fades
        # is_controlled: Equals 1 when this entity is under a control spell
        # health: Remaining health of this monster
        # vx: Trajectory of this monster
        # near_base: 0=monster with no target yet, 1=monster targeting a base
        # threat_for: Given this monster's trajectory, is it a threat to 1=your base, 2=your opponent's base, 0=neither
        _id, _type, x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for = [int(j) for j in input().split()]
        if health < 0:
            entity = Entity.create(_id, _type, x, y, shield_life, is_controlled)
        else:
            entity = Monster.create(_id, _type, x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for)
        entities.append(entity)

    my_heroes = [e for e in entities if e.type == 1]
    monsters = [e for e in entities if e.type == 0]

    debug(my_heroes)
    debug([m.p for m in monsters])
    for hero in my_heroes:
        if monsters:
            monster = get_nearest_monster(base_p, monsters)
            target_p = monster.p

            # In the first league: MOVE <x> <y> | WAIT; In later leagues: | SPELL <spellParams>;
            print(f"MOVE {target_p.x} {target_p.y}")
        else:
            # todo not so far
            # todo ideally disperse!
            target_p = 2 * hero.p - base_p
            print(f"MOVE {target_p.x} {target_p.y} away from base")
