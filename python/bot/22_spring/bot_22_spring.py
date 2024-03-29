import dataclasses
import math
import random
import sys
from typing import List

WIDTH, HEIGHT = 17630, 9000
MONSTER_TARGET_RADIUS = 5000
MONSTER_DAMAGE_RADIUS = 300
HERO_DAMAGE_RADIUS = 800
MONSTER_SPEED = 400
HERO_SPEED = 800
WIND_CAST_RANGE = 1280
SPELL_COST = 10
HERO_ATTACK = 2
HERO_FOG = 2200
BASE_FOG = 6000

WANDER_THRES = 6000+2200
CLOSE_DIST_TO_PURSUE = 2200
CLOSE_DIST_TO_WANDER = HEIGHT//2 - HERO_FOG - MONSTER_SPEED  # -MONSTER_SPEED just not to be to on the edge
TURNS_TO_HARASS = 100
MIN_MANA_TO_HARASS = 6 * SPELL_COST
MIN_HEALTH_TO_CONTROL = 5
MIN_HEALTH_TO_SHIELD = 3
DIST_TO_CLOSE_HARASS = BASE_FOG + 1
DIST_TO_GET_EVEN_CLOSER_TO_B2 = MONSTER_TARGET_RADIUS

random.seed(0)


def debug(*texts):
    print(*texts, file=sys.stderr, flush=True)


class Action:
    @staticmethod
    def move(point, text=""):
        return f"MOVE {point.x} {point.y} " + text
    @staticmethod
    def wind(point, text=""):
        return f"SPELL WIND {point.x} {point.y} " + text
    @staticmethod
    def shield(entity, text=""):
        return f"SPELL SHIELD {entity.id} " + text
    @staticmethod
    def control(entity, point, text=""):
        return f"SPELL CONTROL {entity.id} {point.x} {point.y} " + text


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

    def dist(self, other):
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
    def __neg__(self):
        return Point(-self.x, -self.y)
    def round(self, ndigits=None):
        return Point(round(self.x, ndigits), round(self.y, ndigits))


MIDDLE_POINT = Point(WIDTH // 2, HEIGHT // 2)
ZERO_VECTOR = Point(0, 0)


def get_turns_to_base(point):
    dist = point.dist(base_p) - MONSTER_DAMAGE_RADIUS
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
    threat_for: int  # Given this monster's trajectory, is it a threat to 1=your base, 2=your opponent's base, 0=neither
    turns_to_base: int
    winded: bool = False

    @staticmethod
    def create(_id, _type, x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for):
        point = Point(x, y)
        return Monster(_id, _type, point, shield_life, bool(is_controlled), health, Point(vx, vy),
                       bool(near_base), threat_for, get_turns_to_base(point))


def get_nearest_monster(p, monsters):
    min_idx = min(range(len(monsters)), key=lambda i: monsters[i].p.dist(p))
    return monsters[min_idx]


# base_x: The corner of the map representing your base
base_x, base_y = [int(i) for i in input().split()]
base_p = Point(base_x, base_y)
opp_base_p = Point(WIDTH-base_x, HEIGHT-base_y)
# debug(base_p, opp_base_p)

int(input())  # Always 3
i_turn = 1
my_health = my_mana = opp_health = opp_mana = 0
entities = []
prev_heroes = {}


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
    # debug("\n".join([str(m) for m in monsters]))
    attacker, *defenders = my_heroes
    action = attacker_action(attacker)
    print(action)

    for hero in defenders:
        action = best_for_one_hero(hero)
        print(action)


def attacker_action(hero: Entity):
    global my_mana, i_turn
    if i_turn >= TURNS_TO_HARASS and my_mana >= MIN_MANA_TO_HARASS:
        return harass(hero)
    return collect_idle_mana(hero)


def harass(hero: Entity):
    debug("harrasing", hero)
    if hero.p.dist(base_p) <= BASE_FOG:
        return Action.move(opp_base_p, "away from my base")

    for m in monsters:
        m.d = m.p.dist(hero.p)
        m.d2b2 = m.p.dist(opp_base_p)
    close_monsters = [m for m in monsters if m.d <= HERO_FOG]
    close_monsters_heading_for_me = [m for m in close_monsters if m.threat_for == 1 and m.shield_life == 0]
    if close_monsters_heading_for_me:
        return control_farthest_monster_to_opp(close_monsters_heading_for_me)
    close_monsters_roaming = [m for m in close_monsters if m.threat_for == 0 and m.health > MIN_HEALTH_TO_CONTROL and m.shield_life == 0]
    if close_monsters_roaming:
        return control_farthest_monster_to_opp(close_monsters_roaming)

    if hero.p.dist(opp_base_p) > DIST_TO_CLOSE_HARASS:
        return Action.move(opp_base_p, "closer to B2")
    if hero.shield_life == 0:  # cannot get shield earlier than before shield wears down
        return Action.shield(hero)

    # todo better condition probably!
    hero_d2b2 = hero.p.dist(opp_base_p)
    monsters_far_away = [m for m in close_monsters if m.d2b2 > hero_d2b2 and m.d <= WIND_CAST_RANGE and m.shield_life == 0]
    if monsters_far_away:
        return Action.wind(opp_base_p, "fuu")
    monsters_without_shield = [m for m in close_monsters if m.shield_life == 0 and m.health >= MIN_HEALTH_TO_SHIELD]
    if monsters_without_shield:
        best_monster_to_shield = min(monsters_without_shield, key=lambda m: m.d2b2)
        return Action.shield(best_monster_to_shield, f"shield B2 {best_monster_to_shield.id}")
    if hero.p.dist(opp_base_p) > DIST_TO_GET_EVEN_CLOSER_TO_B2:
        return Action.move(opp_base_p, "even closer to B2")

    random_dir = Point(random.randrange(-1, 2, 2) * HERO_SPEED, random.randrange(-1, 2, 2) * HERO_SPEED)
    return Action.move(hero.p + random_dir, "random")


def control_farthest_monster_to_opp(monster_list):
    best_monster_to_control = max(monster_list, key=lambda m: m.d)
    return Action.control(best_monster_to_control, opp_base_p, f"Base2 {best_monster_to_control.id}")


def collect_idle_mana(hero: Entity):
    debug("collecting wild mana")
    if monsters:
        monster = get_nearest_monster(hero.p, monsters)
        if monster.p.dist(hero.p) <= CLOSE_DIST_TO_PURSUE:
            target_p = monster.p
            return Action.move(target_p, f"AM {monster.id}")
    if hero.p.dist(MIDDLE_POINT) > CLOSE_DIST_TO_WANDER:
        return Action.move(MIDDLE_POINT, "")
    return Action.move(hero.p + Point(-1000, 2000), "")


def best_for_one_hero(hero: Entity):
    global my_mana, i_turn
    if monsters:
        monster = get_nearest_monster(base_p, monsters)
        debug("hero", hero)
        debug(monster)
        # debug(monster.turns_to_base)

        if (monster.turns_to_base == 1 and monster.shield_life == 0
                and monster.p.dist(hero.p) < WIND_CAST_RANGE and my_mana >= SPELL_COST and not monster.winded):
            target_p = 2 * hero.p - base_p
            my_mana -= SPELL_COST
            # todo you might want to mark all monsters in neighborhood as well
            monster.winded = True
            return Action.wind(target_p, f"LH{monster.id}")

        prev_hero = prev_heroes.get(hero.id)
        if hero.shield_life == 0 and prev_hero is not None and prev_hero.is_controlled:
            return Action.shield(hero)

        dist_to_attack = hero.p.dist(monster.p) - HERO_DAMAGE_RADIUS
        if dist_to_attack > 0:
            # go to the position where the monster will be - if on that spot, you still hit the monster
            # - also better trajectory when you are distant from it
            # - disadvantage - when killing the monster you are closer to the base, while other monsters usually aren't
            additional_vector = monster.vp
        elif monster.p.dist(base_p) <= MONSTER_TARGET_RADIUS:
            additional_vector = (-1.8 * monster.vp).round()
        else:
            additional_vector = ZERO_VECTOR
        target_p = monster.p + additional_vector

        # In the first league: MOVE <x> <y> | WAIT | SPELL <spellParams>
        return Action.move(target_p, f"mon {monster.id}")

    # todo ideally disperse!
    if hero.p.dist(base_p) > WANDER_THRES - i_turn * 10:
        return Action.move(base_p, "return closer to base")
    else:
        target_p = 2 * hero.p - base_p
        return Action.move(target_p, "away from base")


# game loop
while True:
    load_inputs()
    my_heroes: List[Entity] = [e for e in entities if e.type == 1]
    monsters: List[Monster] = [e for e in entities if e.type == 0]

    do_best_action()
    prev_heroes = {h.id: h for h in my_heroes}
