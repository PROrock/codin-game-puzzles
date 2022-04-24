import dataclasses
import math
import sys

# unused consts:
# WIDTH,HEIGHT = X=17630, Y=9000
# ANTIFOG: base 6000, hero 2200
# MOVE monster 400, hero 800
# monsters target base 5000 units/px
# monster damage base 300 from base
DAMAGE_RADIUS = 300
MONSTER_SPEED = 400
HERO_SPEED = 800
WANDER_THRES = 6000+2200
WIND_CAST_RANGE = 1280
SPELL_COST = 10


def debug(*texts):
    print(*texts, file=sys.stderr, flush=True)


class Action:
    @staticmethod
    def move(point, text=""):
        return f"MOVE {point.x} {point.y} " + text

    @staticmethod
    def wind(point, text=""):
        return f"SPELL WIND {point.x} {point.y} " + text


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


def get_turns_to_base(point):
    dist = point.l2_dist(base_p) - DAMAGE_RADIUS
    return math.ceil(dist / MONSTER_SPEED)


@dataclasses.dataclass(frozen=False)
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


@dataclasses.dataclass(frozen=False)
class Monster(Entity):
    health: int
    vp: Point
    near_base: bool
    threat_for: int
    turns_to_base: int
    winded: bool = False

    @staticmethod
    def create(_id, _type, x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for):
        point = Point(x, y)
        return Monster(_id, _type, point, shield_life, bool(is_controlled), health, Point(vx, vy),
                       bool(near_base), threat_for, get_turns_to_base(point))


def get_nearest_monster(p, monsters):
    min_idx = min(range(len(monsters)), key=lambda i: monsters[i].p.l2_dist(p))
    return monsters[min_idx]


# base_x: The corner of the map representing your base
base_x, base_y = [int(i) for i in input().split()]
base_p = Point(base_x, base_y)
heroes_per_player = int(input())  # Always 3
i_turn = 1
my_health = my_mana = opp_health = opp_mana = 0
entities = []


def load_inputs():
    global i_turn
    global entities
    entities = []
    i_turn += 1

    global my_health, my_mana, opp_health, opp_mana
    my_health, my_mana = [int(j) for j in input().split()]
    opp_health, opp_mana = [int(j) for j in input().split()]
    entity_count = int(input())  # Amount of heroes and monsters you can see
    for _ in range(entity_count):
        # _type: 0=monster, 1=your hero, 2=opponent hero
        # shield_life: Count down until shield spell fades. 0 if no shield
        # is_controlled: Equals 1 when this entity is under a control spell
        # near_base: 0=monster with no target yet, 1=monster targeting a base
        # threat_for: Given this monster's trajectory, is it a threat to 1=your base, 2=your opponent's base, 0=neither
        _id, _type, x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for = [int(j) for j in input().split()]
        if health < 0:
            entity = Entity.create(_id, _type, x, y, shield_life, is_controlled)
        else:
            entity = Monster.create(_id, _type, x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for)
        entities.append(entity)


def do_best_action():
    # debug(my_heroes)
    debug([m.p for m in monsters])

    for hero in my_heroes:
        action = best_for_one_hero(hero)
        print(action)


def best_for_one_hero(hero):
    global my_mana
    if monsters:
        monster = get_nearest_monster(base_p, monsters)
        debug(monster)
        debug(monster.turns_to_base)

        if (monster.turns_to_base == 1 and monster.shield_life == 0
                and monster.p.l2_dist(hero.p) < WIND_CAST_RANGE and my_mana >= SPELL_COST and not monster.winded):
            target_p = 2 * hero.p - base_p
            my_mana -= SPELL_COST
            # todo you might want to mark all monsters in neighborhood as well
            monster.winded = True
            return Action.wind(target_p, f"LH{monster.id}")

        # go to the position where the monster will be - if on that spot, you still hit the monster
        # - also better trajectory when you are distant from it
        # - disadvantage - when killing the monster you are closer to the base, while other monsters usually aren't
        target_p = monster.p + monster.vp

        # In the first league: MOVE <x> <y> | WAIT | SPELL <spellParams>
        return Action.move(target_p, f"mon {monster.id}")

    # todo ideally disperse!
    if hero.p.l2_dist(base_p) > WANDER_THRES - i_turn * 10:
        return Action.move(base_p, "return closer to base")
    else:
        target_p = 2 * hero.p - base_p
        return Action.move(target_p, "away from base")


# game loop
while True:
    load_inputs()
    my_heroes = [e for e in entities if e.type == 1]
    monsters = [e for e in entities if e.type == 0]

    do_best_action()
