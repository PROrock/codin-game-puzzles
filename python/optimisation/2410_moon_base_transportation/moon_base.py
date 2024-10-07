# 222995 - default
# 447865 - loop the default pod
# 732601 - naive tube and pod (back-and-forth in 1 segment) heuristic

from collections import defaultdict
import math
import sys
from dataclasses import dataclass
from typing import Counter, NamedTuple, List


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
    def from_input(building_integers):
        type_, id, x, y, *rest = building_integers
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


resources = -1
travel_lines = []
pods = {}
buildings = {}
landing_by_type = {}
dorm_by_type = {}


def buildings_by_type(buildings):
    landing_by_type, dorm_by_type = defaultdict(list), defaultdict(list)
    for building in buildings.values():
        if building.type_ == Building.LANDING:
            for type in dict(building.astronauts.most_common()).keys():
                landing_by_type[type].append(building)
        else:
            dorm_by_type[building.type_].append(building)
    return landing_by_type, dorm_by_type

def build_travel_dict(travel_lines):
    travel_dict = defaultdict(list)
    for line in travel_lines:
        travel_dict[line.build1].append((line.build2, line))
    return travel_dict


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
    travel_dict = build_travel_dict(travel_lines)

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

    debug(new_buildings)
    debug(travel_lines)
    debug(buildings)
    debug("landing_by_type", landing_by_type)
    debug(dorm_by_type)
    debug(travel_dict)

    new_tubes = []
    for type, landings in landing_by_type.items():
        for landing in landings:
            for dorm in dorm_by_type[type]:
                new_tubes.append(Tube(landing.id, dorm.id))

    new_pod_id = len(pods)
    new_pods = []
    for landings in landing_by_type.values():
        for landing in landings:
            for dest_id, line in travel_dict.get(landing.id, []):
                new_pods.append(Pod(new_pod_id, [landing.id, dest_id, landing.id]))
                new_pod_id += 1

    actions = [tube.to_action() for tube in new_tubes] + [pod.to_action() for pod in new_pods]
    print(";".join(actions))
