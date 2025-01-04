import sys
import math
from dataclasses import dataclass
from typing import NamedTuple


def debug(*s):
    print(*s, file=sys.stderr, flush=True)

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

@dataclass
class Entity:
    pos: Vect
    type_: str
    owner: int
    organ_id: int
    organ_dir: str
    organ_parent_id: int
    organ_root_id: int

def a_grow(id_, pos, type_):
    return f"GROW {id_} {pos.x} {pos.y} {type_}"

def argmin(iterable):
    return min(enumerate(iterable), key=lambda t:t[1])[0]


width, height = [int(i) for i in input().split()]

# game loop
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

    # my_d: your protein stock
    my_a, my_b, my_c, my_d = [int(i) for i in input().split()]
    # opp_d: opponent's protein stock
    opp_a, opp_b, opp_c, opp_d = [int(i) for i in input().split()]
    required_actions_count = int(input())  # your number of organisms, output an action for each one in any order
    for i in range(required_actions_count):
        my_org = [e for e in entities if e.owner == 1][0]
        first_p = [e for e in entities if e.type_ == "A"][0]

        print(a_grow(my_org.organ_id, first_p.pos, "BASIC"))
        # print("WAIT")
