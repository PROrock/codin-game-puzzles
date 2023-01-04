import dataclasses
import math
import random
import sys
from typing import Optional

random.seed(0)

N_OF_WANTED_RECYCLERS = 2


class Vect:
    """Immutable 2D vector"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def l1dist(self, other_vect):
        d = abs(self.x-other_vect.x) + abs(self.y-other_vect.y)
        # print(f"l1 dist: {self} and {other_vect} is {d}", file=sys.stderr, flush=True)
        return d

    def l1_norm(self):
        return abs(self.x) + abs(self.y)

    # this doesn't work as len must return integer not float!
    def __len__(self):
        return math.sqrt(self.x**2 + self.y**2)

    def __bool__(self):
        return True

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
    def __mul__(self, multiplier):
        return Vect(self.x * multiplier, self.y * multiplier)
    # right multiplication to support 2 * p
    __rmul__ = __mul__
    def __neg__(self):
        return Vect(-self.x, -self.y)
    def round(self, ndigits=None):
        return Vect(round(self.x, ndigits), round(self.y, ndigits))

@dataclasses.dataclass(frozen=True)
class Tile:
    v: Vect
    scrap_amount: int
    owner: int
    "# owner: 1 = me, 0 = foe, -1 = neutral"
    units: int
    recycler: bool
    can_build: bool
    can_spawn: bool
    in_range_of_recycler: bool

    def __repr__(self):
        return f"T({self.scrap_amount}, {owner}, {units})"

def debug(*s):
    print(*s, file=sys.stderr, flush=True)

def move(amount: int, from_: Vect, to: Vect):
    return f"MOVE {amount} {from_.x} {from_.y} {to.x} {to.y}"

def spawn(amount: int, vect: Vect):
    return f"SPAWN {amount} {vect.x} {vect.y}"

def build(vect: Vect):
    return f"BUILD {vect.x} {vect.y}"

def get_tile(v):
    if not 0 <= v.x < width or not 0 <= v.y < height:
        return None
    # debug(f"map q: {v} {width=} {height=} {0 > v.x >= width=} {v.x >= width}")
    return map[v.y][v.x]

width, height = [int(i) for i in input().split()]
i_turn = 0

while True:
    actions = []
    my_first_spawn_tile: Optional[Vect] = None
    map = []
    my_tiles = []
    non_my_tiles = []
    my_units = []
    my_recyclers = []

    my_matter, opp_matter = [int(i) for i in input().split()]
    for i in range(height):
        map_row = []
        for j in range(width):
            v = Vect(j, i)
            # owner: 1 = me, 0 = foe, -1 = neutral
            scrap_amount, owner, units, recycler, can_build, can_spawn, in_range_of_recycler = [int(k) for k in input().split()]
            tile = Tile(v, scrap_amount, owner, units, bool(recycler), bool(can_build), bool(can_spawn), bool(in_range_of_recycler))
            map_row.append(tile)
            if my_first_spawn_tile is None and tile.can_spawn:
                my_first_spawn_tile = v
            if tile.owner == 1:
                my_tiles.append(tile)
                if tile.units:
                    my_units.append(tile)
                if tile.recycler:
                    my_recyclers.append(tile)
            else:
                non_my_tiles.append(tile)

        map.append(map_row)

    # debug(my_matter, opp_matter)
    # debug([(tile.v.x, tile.v.y, tile.units) for tile in my_units])
    # debug(f"I have {len(my_tiles)} tiles, {len(my_recyclers)} recyclers, "
    #       f"{len(my_units)} unit tiles, {sum(tile.units for tile in my_units)} units")

    move_candidates = [tile for tile in non_my_tiles if tile.scrap_amount > 0]
    if len(move_candidates):
        for tile in my_units:
            neighbour_vs = [Vect(x,y) for x,y in zip([1,-1,0,0], [0,0,1,-1])]
            non_my_neighbours = [n_tile for neighbour_v in neighbour_vs if (n_tile := get_tile(tile.v + neighbour_v)) and n_tile.owner != 1 and n_tile.scrap_amount > 0]
            # not rly nice, but ok
            if len(non_my_neighbours):
                move_candidates = non_my_neighbours
            # if tile.units >= 3:
            n_moves = min(tile.units // 3, 4) + 1
            for _ in range(n_moves):
                index = (tile.v.y*width + tile.v.x + random.randint(0, 1)) % len(move_candidates)
                target = move_candidates[index].v
                # target = random.choice(move_candidates).v
                units_to_move = tile.units // n_moves
                actions.append(move(units_to_move, tile.v, target))

    my_actual_matter = my_matter
    tens_of_matter = my_matter // 10

    spawn_candidates = [tile for tile in my_tiles if tile.can_spawn]
    spawn_candidates_no_units = [tile for tile in spawn_candidates if not tile.units]
    # debug(f"{len(spawn_candidates_no_units)=}")

    possible_build_tiles = [tile for tile in my_tiles if tile.can_build]
    n_recycler_to_build = min(N_OF_WANTED_RECYCLERS - len(my_recyclers), len(possible_build_tiles), tens_of_matter)
    if n_recycler_to_build and len(my_tiles) >= 7 and len(spawn_candidates_no_units) >= 4 and i_turn <= 150:
        tiles_to_build_on = random.sample(possible_build_tiles, n_recycler_to_build)
        for tile_to_build_on in tiles_to_build_on:
            actions.append(build(tile_to_build_on.v))
            my_actual_matter -= 10

    spawn_units = my_actual_matter // 10
    # todo fix not spawn where i try to build - but is it error or just silent?
    if spawn_units:
        if len(spawn_candidates_no_units):
            spawn_candidates = spawn_candidates_no_units
        target = random.choice(spawn_candidates).v
        actions.append(spawn(spawn_units, target))

    print(";".join(actions))
    i_turn += 1
