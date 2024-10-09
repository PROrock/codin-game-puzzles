# 222995 - default
# 447865 - loop the default pod
# 732601 - naive tube and pod (back-and-forth in 1 segment) heuristic
# 1626119 - slight speed optimizations, 100% of TCs yay!
# 1741860 - another optimizations
# 1741860 - no timeouts thanks to: str ids, compute and build just pods, u can afford

# dorm = lunar module

import time
from collections import defaultdict
import math
import sys
from dataclasses import dataclass
from typing import Counter, NamedTuple, List


def debug(*s):
    if False:
        print(*s, file=sys.stderr, flush=True)

@dataclass(frozen=True)
class Tube:
    build1: str
    build2: str
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

@dataclass(frozen=True)
class Building:
    type_: str
    id: str
    vect: Vect
    astronauts: Counter
    LANDING = "0"

    @staticmethod
    def from_input(building_line):
        type_, id, x, y, *rest = building_line
        astronauts = Counter(rest[1:]) if rest else Counter()
        return Building(type_, id, Vect(int(x), int(y)), astronauts)

    def __repr__(self):
        return f"B({self.type_}, {self.id}, {self.vect}, {self.astronauts.most_common()})"


@dataclass(frozen=True)
class Pod:
    id: str
    buildings: List[str]

    def to_action(self):
        return f"POD {self.id} {' '.join(self.buildings)}"


resources = -1
travel_lines = []
new_buildings = {}
landing_by_type = {}
dorm_by_type = {}


def buildings_by_type(buildings):
    landing_by_type, dorm_by_type = defaultdict(list), defaultdict(list)
    for building in buildings.values():
        if building.type_ == Building.LANDING:
            for type in building.astronauts:
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
    start = time.perf_counter_ns()

    num_travel_routes = int(input())
    for i in range(num_travel_routes):
        building_id_1, building_id_2, capacity = input().split()
        travel_lines.append(Tube(building_id_1, building_id_2, int(capacity)))
    travel_dict = build_travel_dict(travel_lines)

    num_pods = int(input())
    for i in range(num_pods):
        _ = input()

    num_new_buildings = int(input())
    new_buildings = {}
    for i in range(num_new_buildings):
        building_properties = input().split()
        building = Building.from_input(building_properties)
        new_buildings[building.id] = building
    landing_by_type, dorm_by_type = buildings_by_type(new_buildings)

    read_done = time.perf_counter_ns()
    debug("read-only all", (read_done-start)/1_000_000)

    # debug(new_buildings)
    # debug(travel_lines)
    # debug("landing_by_type", landing_by_type)
    # debug(dorm_by_type)
    # debug(travel_dict)

    new_tubes = []
    for type, landings in landing_by_type.items():
        for landing in landings:
            # TBD: closest dorm at least?
            dorm = dorm_by_type[type][0] if len(dorm_by_type[type]) else None
            if dorm:
                new_tubes.append(Tube(landing.id, dorm.id))

    new_pods = []
    # TBD: solve also available after building tubes
    available_new_pods = resources // 1000
    new_pod_id = num_pods
    for start_id, end_tuples in travel_dict.items():
        for end_tuple in end_tuples:
            if available_new_pods == 0:
                break

            dest_id, line = end_tuple
            new_pods.append(Pod(str(new_pod_id), [start_id, dest_id, start_id]))
            new_pod_id += 1
            available_new_pods -= 1

    actions = [tube.to_action() for tube in new_tubes] + [pod.to_action() for pod in new_pods]
    print(";".join(actions) if len(actions) else "WAIT")

    end = time.perf_counter_ns()
    debug("heur-only all", (end-read_done)/1_000_000)
    debug("elapsed   all", (end-start)/1_000_000)

    # todo
    # time.sleep(2000)

# next best step would be to stop creating pod on the same tube w/o increasing the capacity, but I don't have time :-/
