from dataclasses import dataclass

import sys


def debug(text):
    print(text, file=sys.stderr,flush=True)


@dataclass(frozen=True)
class Tree:
    cell_index: int
    size: int
    is_mine: bool
    is_dormant: bool

@dataclass(frozen=True)
class Cell:
    cell_index: int
    richness: int
    neighs: tuple


cells = {}
trees = {}


number_of_cells = int(input())  # 37
for i in range(number_of_cells):
    # index: 0 is the center cell, the next cells spiral outwards
    # richness: 0 if the cell is unusable, 1-3 for usable cells
    # neigh_0: the index of the neighbouring cell for each direction
    index, richness, *neighs = [int(j) for j in input().split()]
    cells[index] = Cell(index, richness, neighs)

# game loop
while True:
    best_tree = None

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
        cell_index = int(inputs[0])  # location of this tree
        size = int(inputs[1])  # size of this tree: 0-3
        is_mine = inputs[2] != "0"  # 1 if this is your tree
        is_dormant = inputs[3] != "0"  # 1 if this tree is dormant

        trees[cell_index] = Tree(cell_index, size, is_mine, is_dormant)

    number_of_possible_actions = int(input())  # all legal actions
    for i in range(number_of_possible_actions):
        possible_action = input()  # try printing something from here to start with

    my_trees = [t for t in trees.values() if t.is_mine]
    best_tree = sorted(my_trees, key=lambda t:cells[t.cell_index].richness, reverse=True)[0].cell_index

    # GROW cellIdx | SEED sourceIdx targetIdx | COMPLETE cellIdx | WAIT <message>
    if sun >= 4:
        print(f"COMPLETE {best_tree}")
    else:
        print("WAIT")
