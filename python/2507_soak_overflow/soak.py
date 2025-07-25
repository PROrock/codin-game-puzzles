import sys
import math

from typing import NamedTuple, Any, List, Optional, Literal
from dataclasses import dataclass

# predtim z gitu to lze vzit
# 25.7. 1556-1705

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
        return math.hypot(*result_vect)

grid = []
def elem_at_pos(grid: List[Any], pos: Vect):
    return grid[pos.y][pos.x]

def inbounds(grid: List[Any], pos: Vect):
    return 0 <= pos.x < len(grid[0]) and 0 <= pos.y < len(grid)

def debug_grid(grid):
    debug("GRID")
    for line in grid:
        debug("".join([str(c) for c in line]))
    debug("GRID END")

ARR_TO_VECT = {
    "^": Vect(0, -1),
    ">": Vect(1, 0),
    "v": Vect(0, 1),
    "<": Vect(-1, 0),
}
VECT_TO_ARR = {v:a for a,v in ARR_TO_VECT.items()}
VECTS_CLOCKWISE = list(ARR_TO_VECT.values())

def expand(grid, pos):
    children = []
    for dir_ in VECTS_CLOCKWISE:
        new_pos = pos + dir_
        if inbounds(grid, new_pos):
            children.append(new_pos)
    return children

def neighbours(p: Vect):
    kids = expand(grid, p)
    return {n: elem_at_pos(grid, n) for n in kids}

# from enum import Enum 
# class Cover(Enum):
#     LEFT = ("<", lambda v: v.x < ???)

#     def __init__(self, symbol: str, applies_func):
#         self.symbol = symbol
#         self.applies = applies_func

@dataclass
class Cover:
    p: Vect
    height: float
    direction: str

    def applies(self, enemy_pos: Vect):
        if self.direction == "<":
            return enemy_pos.x < self.p.x
        elif self.direction == ">":
            return enemy_pos.x > self.p.x
        elif self.direction == "^":
            return enemy_pos.y < self.p.y
        else:
            return enemy_pos.y > self.p.y

    @staticmethod
    def left(cover_pos: Vect):
        left_inner = lambda enemy_pos: enemy_pos.x < cover_pos.x
        return left_inner

    @staticmethod
    def right(cover_pos: Vect):
        return lambda enemy_pos: enemy_pos.x > cover_pos.x


@dataclass
class Agent:
    id: int
    player: int
    shoot_cooldown: int
    optimal_range: int
    soaking_power: int
    splash_bombs: int
    p: Optional[Vect]
    cooldown: Optional[int]
    wetness: Optional[int]

    def is_mine(self, my_id: int):
        return self.player == my_id

class A:
    @staticmethod
    def move(v: Vect):
        return f"MOVE {v.x} {v.y}"

    @staticmethod
    def shoot(agent_id: int):
        return f"SHOOT {agent_id}"

######

class Move(NamedTuple):
    p: Vect
    covers: list[Cover]

class Shoot(NamedTuple):
    enemy: Agent
    covers: list[Cover]

def get_covers(p: Vect):
    covers = []
    candidates = expand(grid, p)
    for c in candidates:
        if (tile := elem_at_pos(grid, c)) > 0:
            covers.append(Cover(c, (tile+1)/4, VECT_TO_ARR[c-p]))
    return covers

def get_moves(agent_p: Vect):
    moves = []
    possibles = expand(grid, agent_p)
    for poss in possibles:
        if elem_at_pos(grid, poss) > 0:
            continue  # cover
        covers = get_covers(poss)
        moves.append(Move(poss, covers))
    return moves

def get_max_cover_move(agent_p: Vect, enemies):
    moves = get_moves(agent_p)
    sorted_moves = list(reversed(sorted(moves, key=lambda m: m.covers[0].height)))
    return sorted_moves[0].p
    # todo enemies
        # for e in enemies:
        #     # todo
        #     cover = 0

def get_min_cover_enemy(agent_p: Vect, enemies):
    shoots = [Shoot(e, get_covers(e.p)) for e in enemies]
    # todo no Cover -> list out of range
    sorted_shoots = list(sorted(shoots, key=lambda m: m.covers[0].height))
    return sorted_shoots[0].enemy
    # todo enemies


# Win the water fight by controlling the most territory, or out-soak your opponent!

my_id = int(input())  # Your player id (0 or 1)
agent_data_count = int(input())  # Total number of agents in the game
orig_agents = {}
for i in range(agent_data_count):
    # agent_id: Unique identifier for this agent
    # player: Player id of this agent
    # shoot_cooldown: Number of turns between each of this agent's shots
    # optimal_range: Maximum manhattan distance for greatest damage output
    # soaking_power: Damage output within optimal conditions
    # splash_bombs: Number of splash bombs this can throw this game
    agent_id, player, shoot_cooldown, optimal_range, soaking_power, splash_bombs = [int(j) for j in input().split()]
    orig_agents[agent_id] = Agent(agent_id, player, shoot_cooldown, optimal_range, soaking_power, splash_bombs, None, None, None)
# width: Width of the game map
# height: Height of the game map
width, height = [int(i) for i in input().split()]
for i in range(height):
    line = []
    inputs = input().split()
    for j in range(width):
        # x: X coordinate, 0 is left edge
        # y: Y coordinate, 0 is top edge
        x = int(inputs[3*j])
        y = int(inputs[3*j+1])
        tile_type = int(inputs[3*j+2])
        line.append(tile_type)
    grid.append(line)

# debug_grid(grid)

# game loop
while True:
    agents = {}
    agent_count = int(input())  # Total number of agents still in the game
    for i in range(agent_count):
        # cooldown: Number of turns before this agent can shoot
        # wetness: Damage (0-100) this agent has taken
        agent_id, x, y, cooldown, splash_bombs, wetness = [int(j) for j in input().split()]
        u = orig_agents[agent_id]

        u.p = Vect(x,y)
        u.cooldown = cooldown
        u.splash_bombs = splash_bombs
        u.wetness = wetness
        agents[agent_id] = u

    my_agent_count = int(input())  # Number of alive agents controlled by you
    mine = [a for a in agents.values() if a.is_mine(my_id)]
    enemies = [a for a in agents.values() if not a.is_mine(my_id)]
    debug(mine)
    for a in mine:

        # todo        
        max_cover = get_max_cover_move(a.p, enemies)

        close_enemies = [e for e in enemies if a.p.l2_dist(e.p) <= a.optimal_range]
        if not close_enemies:
            # todo 2x optimal_range
            close_enemies = enemies

        least_protected = get_min_cover_enemy(a.p, close_enemies)
        # wettest = max(enemies, key=lambda a: a.wetness)

        
        actions = [A.move(max_cover), A.shoot(least_protected.id)]
        print(";".join(actions))
        # print(f"{a.id};{action}")
        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr, flush=True)

        # One line per agent: <agentId>;<action1;action2;...> actions are "MOVE x y | SHOOT id | THROW x y | HUNKER_DOWN | MESSAGE text"
        #print("HUNKER_DOWN")
