from collections import defaultdict

import sys


def debug(text):
    print(text, file=sys.stderr, flush=True)

graph = defaultdict(list)

def conn_comp():
    i = 0
    comps = {}

    vertices = set(graph.keys())
    while vertices:
        comp = set()
        i += 1
        debug(f"i={i}")
        v = next(iter(vertices))
        q = {v}
        while q:
            vert = q.pop()
            debug(vert)
            neighbors = graph[vert]
            q.update(n for n in neighbors if n not in comp)
            vertices.remove(vert)
            comp.add(vert)
        comps[i] = comp
    return i, comps


def get_tiles(component):
    s = sum(len(graph[v]) - 2 for v in component)
    return 1 if s == 0 else s / 2 + 1


def get_all_tiles(component_dict):
    c = 0
    for component in component_dict.values():
        tiles = get_tiles(component)
        debug(f"{component}, {tiles}")
        c += tiles
    return c


e = int(input())
for i in range(e):
    a, b = [int(j) for j in input().split()]
    graph[a].append(b)
    graph[b].append(a)

for v, neighbors in graph.items():
    debug(f"{v}, {neighbors}")

comps = conn_comp()
components = comps[1]
t = int(get_all_tiles(components))

print(f"{comps[0]} {t}")
