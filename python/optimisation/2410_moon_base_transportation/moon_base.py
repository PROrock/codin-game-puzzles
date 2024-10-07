# 222995 - default
# 447865 - loop the default pod

import math
import sys
from dataclasses import dataclass
from typing import Counter, NamedTuple, List

I = 0


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
    LANDING = 0

    @staticmethod
    def from_input(bulding_integers):
        type_, id, x, y, *rest = bulding_integers
        astronauts = Counter(rest[1:]) if rest else Counter()
        return Building(type_, id, Vect(x, y), astronauts)

    def __repr__(self):
        return f"B({self.type_}, {self.id}, {self.vect}, {self.astronauts.most_common()})"


@dataclass
class Pod:
    id: int
    buildings: List[int]

    def to_action(self):
        return f"POD {self.id} {' '.join([str(building) for building in self.buildings])}"


resources=-1
travel_lines=[]
pods={}
buildings={}
landing_by_type={}
dorm_by_type={}


def buildings_by_type(buildings):
    landing_by_type, dorm_by_type = {}, {}
    for building in buildings.values():
        dict_to_add = landing_by_type if building.type_ == Building.LANDING else dorm_by_type
        dict_to_add[building.type_] = building
    return landing_by_type, dorm_by_type


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
    travel_dict = {line1.build1: (line1.build2, line1) for line1 in travel_lines}
        
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
    landing_by_type, dorm_by_type = buildings_by_type(buildings)


    debug(travel_lines)
    debug(buildings)

    new_tubes = []
    for type, landing in landing_by_type.items():
        for dorm in dorm_by_type[type]:
            new_tubes.append(Tube(landing.id, dorm.id))

    new_pod_id = len(pods)
    new_pods = []
    for type, landing in landing_by_type.values():
        for dest, line in travel_dict[landing.id]:
            new_pods.append(Pod(new_pod_id, [landing.id, dest.id, landing.id]))
            new_pod_id += 1

    actions = [tube.to_action() for tube in new_tubes] + [pod.to_action() for pod in new_pods]
    print(";".join(actions))
    # TUBE | UPGRADE | TELEPORT | POD | DESTROY | WAIT
    # print("TUBE 0 1;TUBE 0 2;POD 42 0 1 0 2 0")
