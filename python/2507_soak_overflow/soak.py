import sys
import math

from typing import NamedTuple, Any, List

WALL = "#"
EMPTY = "."

class A:
    @staticmethod
    def move(v):
        return f"MOVE {v.x} {v.y}"

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
        return math.hypot(result_vect)


# Win the water fight by controlling the most territory, or out-soak your opponent!

my_id = int(input())  # Your player id (0 or 1)
agent_data_count = int(input())  # Total number of agents in the game
for i in range(agent_data_count):
    # agent_id: Unique identifier for this agent
    # player: Player id of this agent
    # shoot_cooldown: Number of turns between each of this agent's shots
    # optimal_range: Maximum manhattan distance for greatest damage output
    # soaking_power: Damage output within optimal conditions
    # splash_bombs: Number of splash bombs this can throw this game
    agent_id, player, shoot_cooldown, optimal_range, soaking_power, splash_bombs = [int(j) for j in input().split()]
# width: Width of the game map
# height: Height of the game map
width, height = [int(i) for i in input().split()]
for i in range(height):
    inputs = input().split()
    for j in range(width):
        # x: X coordinate, 0 is left edge
        # y: Y coordinate, 0 is top edge
        x = int(inputs[3*j])
        y = int(inputs[3*j+1])
        tile_type = int(inputs[3*j+2])

# game loop
while True:
    goals = [Vect(6,1),Vect(6,3)]
    agent_count = int(input())  # Total number of agents still in the game
    for i in range(agent_count):
        # cooldown: Number of turns before this agent can shoot
        # wetness: Damage (0-100) this agent has taken
        agent_id, x, y, cooldown, splash_bombs, wetness = [int(j) for j in input().split()]
    my_agent_count = int(input())  # Number of alive agents controlled by you
    for i in range(my_agent_count):
        print(A.move(goals.pop()))
        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr, flush=True)


        # One line per agent: <agentId>;<action1;action2;...> actions are "MOVE x y | SHOOT id | THROW x y | HUNKER_DOWN | MESSAGE text"
        #print("HUNKER_DOWN")
