# 222995 - default
# 447865 - loop the default pod

import sys
import math

def debug(*s):
    print(*s, file=sys.stderr, flush=True)


resources=-1
travel_routes={}
pods={}
buildings={}



# game loop
while True:
    resources = int(input())
    num_travel_routes = int(input())
    for i in range(num_travel_routes):
        building_id_1, building_id_2, capacity = [int(j) for j in input().split()]
    num_pods = int(input())
    for i in range(num_pods):
        pod_properties = input()
    num_new_buildings = int(input())
    for i in range(num_new_buildings):
        building_properties = input()


    # TUBE | UPGRADE | TELEPORT | POD | DESTROY | WAIT
    print("TUBE 0 1;TUBE 0 2;POD 42 0 1 0 2 0")
