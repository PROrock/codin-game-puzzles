# 222995 - default
# 447865 - loop the default pod

import sys
import math
from dataclasses import dataclass
from typing import Counter, NamedTuple

def debug(*s):
    print(*s, file=sys.stderr, flush=True)

@dataclass(frozen=True)
class Tube:
    build1: int
    build2: int
    capacity: int = 1
    
    def __repr__(self):
        return f"T({self.build1}-{self.build2}, c={self.capacity})"

    def to_action(self):
        return f"TUBE {self.build1} {self.build2}"

class Vect(NamedTuple):
    x: int
    y: int


    def __add__(self, other):
        return Vect(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vect(self.x - other.x, self.y - other.y)

    def l2_dist(self, other):
        result_vect = other-self
        return math.hypot(result_vect)

@dataclass
class Building:
    type_: int
    id: int
    vect: Vect
    astronauts: Counter

    @staticmethod
    def from_input(bulding_integers):
        type_, id, x, y, *rest = bulding_integers
        astronauts = Counter(rest[1:]) if rest else Counter()
        return Building(type_, id, Vect(x, y), astronauts)

resources=-1
travel_lines=[]
pods={}
buildings={}



# game loop
while True:
    resources = int(input())
    num_travel_routes = int(input())
    for i in range(num_travel_routes):
        building_id_1, building_id_2, capacity = [int(j) for j in input().split()]
        if capacity == 0:
            # todo teleport
            line = Tube(building_id_1, building_id_2, capacity)
        else:
            line = Tube(building_id_1, building_id_2, capacity)
        travel_lines.append(line)
        
    num_pods = int(input())
    for i in range(num_pods):
        pod_properties = input()
    num_new_buildings = int(input())
    new_buildings = []
    for i in range(num_new_buildings):
        building_properties = [int(x) for x in input().split()]
        building = Building.from_input(building_properties)
        new_buildings.append(building)
        buildings[building.id] = building

    debug(travel_lines)
    debug(buildings)

    # todo heuristic w/o detection

    # TUBE | UPGRADE | TELEPORT | POD | DESTROY | WAIT
    print("TUBE 0 1;TUBE 0 2;POD 42 0 1 0 2 0")
