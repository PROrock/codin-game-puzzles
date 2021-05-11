from dataclasses import dataclass

import sys

MAX_DAY = 23
MAX_SIZE = 3
COSTS = (0, 1, 3, 7)


def debug(text):
    print(text, file=sys.stderr,flush=True)


@dataclass(frozen=True)
class Tree:
    id: int
    size: int
    is_mine: bool
    is_dormant: bool

@dataclass(frozen=True)
class Cell:
    id: int
    richness: int
    neighs: tuple


cells = {}
trees = {}


def grow_cost(my_trees, target_size):
    return COSTS[target_size] + len(t for t in my_trees if t.size == target_size)

def best_action():
    # GROW cellIdx | SEED sourceIdx targetIdx | COMPLETE cellIdx | WAIT <message>
    my_trees = [t for t in trees.values() if t.is_mine]

    # if it's not the last day, invest in the future
    if day < MAX_DAY:
        # grow the tree, if there is any
        for t in my_trees:
            if t.size < MAX_SIZE and not t.is_dormant:
                # cost = grow_cost(my_trees, t.size+1)
                return f"GROW {t.id}"

        # plant seed if you can
        # cost = grow_cost(my_trees, 0)
        all_plantable_cells = [(t, cells[n])
                               for t in my_trees
                               if not t.is_dormant
                               for n in cells[t.id].neighs
                               if n and cells[n].richness > 0 and n not in trees.keys()]
        if all_plantable_cells:
            best_seed_tree, best_seed = sorted(all_plantable_cells, key=lambda tup: tup[1].richness, reverse=True)[0]
            return f"SEED {best_seed_tree.id} {best_seed.id}"

    # cut down, if you can (called more or less only on last day)
    my_big_trees = [t for t in my_trees if t.size == MAX_SIZE]
    if sun >= 4 and my_big_trees:
        best_tree = sorted(my_big_trees, key=lambda t:cells[t.id].richness, reverse=True)[0].id
        return f"COMPLETE {best_tree}"
    else:
        return "WAIT"



number_of_cells = int(input())  # 37
for i in range(number_of_cells):
    # index: 0 is the center cell, the next cells spiral outwards
    # richness: 0 if the cell is unusable, 1-3 for usable cells
    # neigh_0: the index of the neighbouring cell for each direction
    index, richness, *neighs = [int(j) for j in input().split()]
    cells[index] = Cell(index, richness, tuple(None if n == -1 else n for n in neighs))

# game loop
while True:
    trees = {}

    day = int(input())  # the game lasts 24 days: 0-23
    nutrients = int(input())  # the base score you gain from the next COMPLETE action
    # sun: your sun points
    # score: your current score
    sun, score = [int(i) for i in input().split()]
    inputs = input().split()
    opp_sun = int(inputs[0])  # opponent's sun points
    opp_score = int(inputs[1])  # opponent's score
    opp_is_waiting = inputs[2] != "0"  # whether your opponent is asleep until the next day
    number_of_trees = int(input())  # the current amount of trees
    for i in range(number_of_trees):
        inputs = input().split()
        id = int(inputs[0])  # location of this tree
        size = int(inputs[1])  # size of this tree: 0-3
        is_mine = inputs[2] != "0"  # 1 if this is your tree
        is_dormant = inputs[3] != "0"  # 1 if this tree is dormant

        trees[id] = Tree(id, size, is_mine, is_dormant)

    number_of_possible_actions = int(input())  # all legal actions
    for i in range(number_of_possible_actions):
        possible_action = input()  # try printing something from here to start with

    action = best_action()
    print(action)

