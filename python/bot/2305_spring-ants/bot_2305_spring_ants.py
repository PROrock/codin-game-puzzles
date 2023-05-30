import enum
import sys
from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List

EGG_DIST_THRES = 3


def debug(*s):
    print(*s, file=sys.stderr, flush=True)


@enum.unique
class Type(Enum):
    EMPTY = 0
    EGG = 1
    CRYSTAL = 2


@dataclass
class Cell:
    id: int
    type: Type
    init_resources: int
    neighs: tuple = field(repr=False)
    dist: int
    resources: Optional[int]
    my_ants: Optional[int]
    opp_ants: Optional[int]


class Action:
    @staticmethod
    def line(source_id, target_id, strength):
        return f"LINE {source_id} {target_id} {strength}"
    @staticmethod
    def message(text):
        return f"MESSAGE {text}"


class Node(ABC):
    state: object
    action: object
    n_steps: int = 0
    prev_node: Optional["Node"] = None

    def __repr__(self):
        return f"N({self.state}, {self.action}, {self.n_steps})"

    @abstractmethod
    def expand(self) -> List["Node"]:
        pass

    @abstractmethod
    def process(self):
        pass


class HexNode(Node):
    def __init__(self, cell: Cell, dist: int):
        self.cell = cell
        self.dist = dist
        self.state = cell.id

    def __repr__(self):
        return f"HN({self.cell}, {self.dist})"

    def expand(self) -> List["Node"]:
        return [HexNode(cells[neigh], self.dist+1) for neigh in self.cell.neighs if neigh is not None]

    def process(self):
        self.cell.dist = self.dist


class BreadthFirstTraverse(ABC):
    def search(self, init_state) -> Optional[Node]:
        """Breadth-first search from init_state to goal"""
        visited_states = set()
        queue = deque([self.get_start_node(init_state)])

        while queue:
            node = queue.popleft()
            if node.state not in visited_states:
                node.process()
                new_nodes = node.expand()
                queue.extend(new_nodes)
                visited_states.add(node.state)

                debug(node, new_nodes)
            else:
                debug(f"{node} already visited before!")

        self.debug("goal not reached")
        return None

    @abstractmethod
    def get_start_node(self, init_state) -> Node:
        pass

    @staticmethod
    def debug(*texts):
        return print(*texts, file=sys.stderr, flush=True)


class DistToBaseTraverse(BreadthFirstTraverse):
    def get_start_node(self, init_state) -> Node:
        return HexNode(init_state, 0)


target_cell = None
msg = ""

cells = {}

number_of_cells = int(input())  # amount of hexagonal cells in this map
for i in range(number_of_cells):
    # _type: 0 for empty, 1 for eggs, 2 for crystal
    # initial_resources: the initial amount of eggs/crystals on this cell
    # neigh_0: the index of the neighbouring cell for each direction
    _type, initial_resources, *neighs = [int(j) for j in input().split()]
    cells[i] = Cell(i, Type(_type), initial_resources, tuple([None if n == -1 else n for n in neighs]), -1, None, None, None)
number_of_bases = int(input())
my_bases = [int(i) for i in input().split()]
my_base = my_bases[0]
opp_bases = [int(i) for i in input().split()]
# debug(f"{my_bases=}")
# debug(f"{opp_bases=}")

# compute dist to my base
DistToBaseTraverse().search(cells[my_base])


def act():
    global target_cell, msg
    actions = []
    if target_cell is None or not cells[target_cell.id].resources:
        resources = [cell for cell in cells.values() if cell.resources]
        eggs = sorted([cell for cell in resources if cell.type == Type.EGG], key=lambda c: c.dist)
        if len(eggs) and eggs[0].dist < EGG_DIST_THRES:
            target_cell = eggs[0]
            msg = f"EGG {target_cell}"
        else:
            crystals = [cell for cell in resources if cell.type == Type.CRYSTAL]
            target_cell = min(crystals, key=lambda c: c.dist)
            msg = f"CRY {target_cell}"
    actions.append(Action.line(my_base, target_cell.id, 1))
    actions.append(Action.message(msg))
    return actions


# game loop
while True:
    for i in range(number_of_cells):
        # resources: the current amount of eggs/crystals on this cell
        # my_ants: the amount of your ants on this cell
        # opp_ants: the amount of opponent ants on this cell
        resources, my_ants, opp_ants = [int(j) for j in input().split()]
        cell = cells[i]
        cell.resources, cell.my_ants, cell.opp_ants = resources, my_ants, opp_ants

    actions = act()
    print(";".join(actions))
