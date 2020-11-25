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
    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

# def len_vector(v):
#     return math.sqrt(sum([d*d for d in v]))
#
# def plus_vector(a,b):
#     return (a[0]+b[0], a[1]+b[1])

class Object:
    def __init__(self, id, x, y, xnext=None, ynext=None):
        self.id=id
        self.v=Vect(x,y)
        self.vnext=Vect(xnext,ynext) if xnext is not None and ynext is not None else None
    def __repr__(self):
        return f"Id={self.id}, {self.v}"
        # return f"Id={self.id}, {self.v}, next={self.vnext}"

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

    for h in humans.values():
        z_dists = [(h.v - z.v).length() for z in zombies.values()]
        min_z_dist = min(z_dists)
        # debug(f"Min is {min_z_dist} from {z_dists}")
        h.min_z_dist = min_z_dist
        h.min_z_turns = math.ceil(min_z_dist/ZOMBIE_SPEED)

        h.ash_dist = (h.v - ash).length()
        h.ash_turns = math.ceil((h.ash_dist-ASH_RANGE)/ASH_SPEED)
        h.diff = h.min_z_turns-h.ash_turns

    for h in humans.values():
        debug(f"{h}, a_turns={h.ash_turns}, z_turns={h.min_z_turns}, diff = {h.diff}")

    max_h = max(humans.values(), key=lambda h:h.diff)
    debug(f"Max is {max_h}")
    target_v = max_h.v

    print(f"{target_v.x} {target_v.y}")
