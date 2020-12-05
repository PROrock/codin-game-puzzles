import functools
import operator

import math
import sys

# Save humans, destroy zombies!

ASH_SPEED=1000
ASH_RANGE=2000
ZOMBIE_SPEED=400

def debug(text):
    print(text, file=sys.stderr, flush=True)

class Vect:
    """Immutable 2D vector"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def l1dist(self, other_vect):
        d = abs(self.x-other_vect.x) + abs(self.y-other_vect.y)
        # print(f"l1 dist: {self} and {other_vect} is {d}", file=sys.stderr, flush=True)
        return d

    def __repr__(self):
        return f"V({self.x},{self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __hash__(self):
        return hash((self.x, self.y))

    def __add__(self, other):
        return Vect((self.x + other.x), (self.y + other.y))
    def __sub__(self, other):
        return Vect((self.x - other.x), (self.y - other.y))
    def __truediv__(self, other):
        return Vect(self.x/other, self.y/other)
    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

class Object:
    def __init__(self, id, x, y, xnext=None, ynext=None):
        self.id=id
        self.v=Vect(x,y)
        self.vnext=Vect(xnext,ynext) if xnext is not None and ynext is not None else None
    def __repr__(self):
        return f"Id={self.id}, {self.v}"
        # return f"Id={self.id}, {self.v}, next={self.vnext}"

def centroid(vectors):
    return functools.reduce(operator.add, vectors)/len(vectors)

# game loop
while True:
    humans = {}
    zombies = {}

    x, y = [int(i) for i in input().split()]
    ash=Vect(x,y)

    human_count = int(input())
    for i in range(human_count):
        human_id, human_x, human_y = [int(j) for j in input().split()]
        humans[human_id]=Object(human_id, human_x, human_y)

    zombie_count = int(input())
    for i in range(zombie_count):
        zombie_id, zombie_x, zombie_y, zombie_xnext, zombie_ynext = [int(j) for j in input().split()]
        zombies[zombie_id]=Object(zombie_id, zombie_x, zombie_y, zombie_xnext, zombie_ynext)

    for z in zombies.values():
        z.ash_dist = (z.vnext - ash).length()

    for h in list(humans.values()):  # list() to make copy, so we can delete from it (while iterating over a copy)
        z_dists = [(h.v - z.v).length() for z in zombies.values()]
        min_z_dist = min(z_dists)
        # debug(f"Min is {min_z_dist} from {z_dists}")
        h.min_z_dist = min_z_dist
        h.min_z_turns = math.ceil(min_z_dist/ZOMBIE_SPEED)

        h.ash_dist = (h.v - ash).length()
        h.ash_turns = math.ceil((h.ash_dist-ASH_RANGE)/ASH_SPEED)
        h.diff = h.min_z_turns-h.ash_turns
        if h.diff < 0:
            debug(f"H {h} is unsaveable, forgetting him...")
            del humans[h.id] # can't save unsavable (=too far away from me, too close to a zombie) humans

    for h in humans.values():
        debug(f"{h}, a_turns={h.ash_turns}, z_turns={h.min_z_turns}, diff = {h.diff}")


    # close_zombies_v = [z.vnext for z in zombies.values() if z.ash_dist < 2 * ASH_RANGE]
    # debug([z.ash_dist for z in zombies.values()])
    # debug(close_zombies_v)
    # c = centroid(close_zombies_v) if close_zombies_v else Vect(-ASH_RANGE, -ASH_RANGE)
    # dist_human_z_centroid = (next(iter(humans.values())).v - c).length()
    # debug(f"centroid={c}, dist_human_z_centroid={dist_human_z_centroid}")
    # # todo following cond for < ASH_RANGE is probably too restrictive (not every time!_, but I'm too tired to think about it now
    # if len(humans) == 1 and dist_human_z_centroid < 1 * ASH_RANGE:
    #     # this is nice, but added only lousy 290 points :-(
    #     target_v = c

    if human_id in humans:
        target_v = Vect(human_x, human_y)
    else:
        # todo - take centroid of humans which are close together instead of just one - compute centroid, dist to it and somehow threshold it?
        max_h = max(humans.values(), key=lambda h:h.diff)
        debug(f"Max is {max_h}")
        target_v = max_h.v

    print(f"{int(target_v.x)} {int(target_v.y)}")

    # two main optimisation paths now:
    # focus on saving one human and do one turn multikills -> try to extend to protect one cluster of humans if possible
    # focus on saving as many humans as possible - THIS IS PROBABLY MORE LUCRATIVE IN POINTS I guess
