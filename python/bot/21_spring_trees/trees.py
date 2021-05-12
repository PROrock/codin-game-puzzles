from collections import Counter
from dataclasses import dataclass

import sys

N_DIRS = 6

MAX_DAY = 23
MAX_SIZE = 3
COSTS = (0, 1, 3, 7)
CUT_COST = 4
MAX_TREES_HEUR = 7
MIN_TREES_HEUR = 10
MAX_SEEDS_HEUR = 3


def debug(*text):
    print(*text, file=sys.stderr, flush=True)


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
my_cum = 0
opp_cum = 0


def grow_cost(target_size):
    return COSTS[target_size] + len([t for t in my_trees if t.size == target_size])

def cut():
    i_can_cut = sun >= CUT_COST and counter[3] > 0
    i_want_cut = counter[1] + counter[2] + counter[3] > MIN_TREES_HEUR or day >= MAX_DAY-1
    if i_can_cut and i_want_cut:
        my_big_trees = [t for t in my_trees if t.size == MAX_SIZE]
        best_tree = sorted(my_big_trees, key=lambda t:cells[t.id].richness, reverse=True)[0].id
        return f"COMPLETE {best_tree}"
    return None

    # good algo for shadows, which are straight, bad for seeds
    # for t in my_trees:
    #     if t.size > 0 and not t.is_dormant:
    #         tree_cell = cells[t.id]
    #         for dir in range(N_DIRS):
    #             n = tree_cell
    #             for _ in range(t.size):
    #                 id = n.neighs[dir]
    #                 if not id:
    #                     break
    #                 n = cells[id]
    #                 if n.richness > 0 and id not in trees.keys():
    #                     yield t, n

def seed_place(tree, cell, depth, result: set, cells_neighbouring_trees):
    if depth <= 0:
        return result
    for n in cell.neighs:
        if n:
            c = cells[n]
            # skip seeds neighbouring with my trees as heuristic
            # if c.richness > 0 and n not in trees.keys() and n not in cells[tree.id].neighs:
            if c.richness > 0 and n not in trees.keys() and n not in cells_neighbouring_trees:
                result.add((tree, c))
            seed_place(tree, c, depth - 1, result, cells_neighbouring_trees)
    return result

def generate_plantable_tuples():
    cells_neighbouring_trees = {n for t in my_trees for n in cells[t.id].neighs}
    for t in my_trees:
        if t.size > 0 and not t.is_dormant:
            tree_cell = cells[t.id]
            seed_tuples = seed_place(t, tree_cell, t.size, set(), cells_neighbouring_trees)
            for seed_tuple in seed_tuples:
                yield seed_tuple

def best_action():
    # GROW cellIdx | SEED sourceIdx targetIdx | COMPLETE cellIdx | WAIT <message>
    # total_cut_cost = counter[3]*CUT_COST

    # cut down, if you can
    action = cut()
    if action:
        return action

    # if it's not the last day, invest in the future
    if day < MAX_DAY: # and counter[1] + counter[2] + counter[3] <= MAX_TREES_HEUR:
        # grow the tree, if there is any
        # todo grow tree on richest soil?
        for t in my_trees:
            if t.size < MAX_SIZE and not t.is_dormant:
                cost = grow_cost(t.size+1)
                if sun >= cost:
                    return f"GROW {t.id}"

        # plant seed if you can
        cost = grow_cost(0)
        if sun >= cost: # and counter[0] < MAX_SEEDS_HEUR:
            all_plantable_cells = list(generate_plantable_tuples())
            debug(len(all_plantable_cells), [(tt.id, cc.id) for tt, cc in all_plantable_cells])
            if all_plantable_cells:
                best_seed_tree, best_seed = sorted(all_plantable_cells, key=lambda tup: tup[1].richness, reverse=True)[0]
                return f"SEED {best_seed_tree.id} {best_seed.id}"

    return "WAIT"



number_of_cells = int(input())  # 37
for i in range(number_of_cells):
    # index: 0 is the center cell, the next cells spiral outwards
    # richness: 0 if the cell is unusable, 1-3 for usable cells
    # neigh_0: the index of the neighbouring cell for each direction
    index, richness, *neighs = [int(j) for j in input().split()]
    cells[index] = Cell(index, richness, tuple(None if n == -1 else n for n in neighs))

prev_day = -1
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

    if day != prev_day:
        prev_day = day
        my_cum += sun
        opp_cum += opp_sun
        debug(day)
    debug(day, my_cum, opp_cum)

    my_trees = [t for t in trees.values() if t.is_mine]
    counter = Counter([t.size for t in my_trees])

    action = best_action()
    print(action + f" {my_cum} {opp_cum}")

