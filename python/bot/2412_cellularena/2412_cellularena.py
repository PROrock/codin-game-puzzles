import sys
import math
from dataclasses import dataclass
from typing import NamedTuple


def debug(*s):
    print(*s, file=sys.stderr, flush=True)

def signum(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0

class Vect(NamedTuple):
    x: int
    y: int

    def invert(self):
        return Vect(-self.x, -self.y)

    def __add__(self, other):
        return Vect(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vect(self.x - other.x, self.y - other.y)

    def __mul__(self, multiplier):
        return Vect(self.x * multiplier, self.y * multiplier)

    def l1_dist(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def l2_dist(self, other):
        result_vect = other - self
        return math.hypot(result_vect)

    def to_unit(self):
        return Vect(signum(self.x), signum(self.y))

DIR_TO_VECT = {
    "N": Vect(0, -1),
    "E": Vect(1, 0),
    "S": Vect(0, 1),
    "W": Vect(-1, 0),
}
VECT_TO_DIR = {v:k for k,v in DIR_TO_VECT.items()}
DIRS_CLOCKWISE = list(DIR_TO_VECT.keys())
VECTS_CLOCKWISE = list(DIR_TO_VECT.values())

def expand(pos):
    children = []
    for dir_ in VECTS_CLOCKWISE:
        new_pos = pos + dir_
        if new_pos not in entity_poss:
            children.append(new_pos)
    return children

@dataclass
class Entity:
    pos: Vect
    type_: str
    owner: int
    organ_id: int
    organ_dir: str
    organ_parent_id: int
    organ_root_id: int

def a_grow(id_, pos, type_, dir_=None):
    d = dir_ if dir_ else ""
    return f"GROW {id_} {pos.x} {pos.y} {type_} {d}"

def argmin(iterable):
    return min(enumerate(iterable), key=lambda t:t[1])[0]


width, height = [int(i) for i in input().split()]

# game loop
def get_nearest(entities, pos):
    amin = argmin([pos.l1_dist(e.pos) for e in entities])
    return entities[amin]


def find_org_and_free_pos(my_orgs, entity_poss):
    for o in my_orgs:
        children = expand(o.pos)
        for c in children:
            if c not in entity_poss:
                return o, c
    return None, None



while True:
    entities = []
    entity_count = int(input())
    for i in range(entity_count):
        inputs = input().split()
        x = int(inputs[0])
        y = int(inputs[1])  # grid coordinate
        _type = inputs[2]  # WALL, ROOT, BASIC, TENTACLE, HARVESTER, SPORER, A, B, C, D
        owner = int(inputs[3])  # 1 if your organ, 0 if enemy organ, -1 if neither
        organ_id = int(inputs[4])  # id of this entity if it's an organ, 0 otherwise
        organ_dir = inputs[5]  # N,E,S,W or X if not an organ
        organ_parent_id = int(inputs[6])
        organ_root_id = int(inputs[7])
        entities.append(Entity(Vect(x,y), _type, owner, organ_id, organ_dir, organ_parent_id, organ_root_id))

    wall_list = [e for e in entities if e.type_ == "WALL"]
    wall_poss = {w.pos for w in wall_list}
    entity_poss = {e.pos for e in entities}

    # my_d: your protein stock
    my_a, my_b, my_c, my_d = [int(i) for i in input().split()]
    # opp_d: opponent's protein stock
    opp_a, opp_b, opp_c, opp_d = [int(i) for i in input().split()]
    required_actions_count = int(input())  # your number of organisms, output an action for each one in any order
    for i in range(required_actions_count):
        a_proteins = [e for e in entities if e.type_ == "A"]
        # first_p = a_proteins[0] if len(a_proteins) else opp_es[0]
        first_p = a_proteins[0] if len(a_proteins) else None

        my_orgs = [e for e in entities if e.owner == 1]
        my_harvesters = [e for e in my_orgs if e.type_ == "HARVESTER"]
        opp_orgs = [e for e in entities if e.owner == 0]

        my_org = [e for e in entities if e.owner == 1][0]
        nearest_my_org = get_nearest(my_orgs, first_p.pos)
        if nearest_my_org.pos.l1_dist(first_p.pos) == 2:
            dir_pos = (first_p.pos - nearest_my_org.pos).to_unit()
            if dir_pos.x != 0:
                dir_pos = Vect(dir_pos.x, 0)

            next_pos = (nearest_my_org.pos + dir_pos)
            d = VECT_TO_DIR[(first_p.pos-next_pos)]
            print(a_grow(nearest_my_org.organ_id, next_pos, "HARVESTER", d))
        elif len(my_harvesters):
            growing_organ, free_pos = find_org_and_free_pos(my_orgs, entity_poss)
            print(a_grow(growing_organ.organ_id, free_pos, "BASIC", ))
        else:
            target = first_p if first_p is not None else opp_orgs[0]
            print(a_grow(nearest_my_org.organ_id, target.pos, "BASIC", ))
        # print("WAIT")
