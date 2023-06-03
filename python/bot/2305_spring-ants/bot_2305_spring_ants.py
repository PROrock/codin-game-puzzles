import enum
import sys
from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List

EGG_DIST_THRES = 3
PARALLEL_CRYSTALS = 2
TARGET_BOOST_MY_ANTS_THRES = 2


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
    neighs: tuple = field(repr=False)
    resources: Optional[int]
    my_ants: Optional[int]
    opp_ants: Optional[int]
    dist: List[int] = field(default_factory=list)


class Action:
    @staticmethod
    def beacon(target_id, strength):
        return f"BEACON {target_id} {strength}"
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
        self.cell.dist.append(self.dist)


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

                # debug(node, new_nodes)
            # else:
                # debug(f"{node} already visited before!")

        # self.debug("goal not reached")
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


target_cells = None

cells = {}

number_of_cells = int(input())  # amount of hexagonal cells in this map
for i in range(number_of_cells):
    _type, initial_resources, *neighs = [int(j) for j in input().split()]
    cells[i] = Cell(i, Type(_type), tuple([n for n in neighs if n != -1]), initial_resources, None, None)
number_of_bases = int(input())
my_bases = [int(i) for i in input().split()]
opp_bases = [int(i) for i in input().split()]

# compute dist to my bases
for my_base in my_bases:
    DistToBaseTraverse().search(cells[my_base])


def act():
    actions = []
    for idx, _ in enumerate(my_bases):
        actions.extend(act_on_one_base(idx))
    return actions


def act_on_one_base(my_base_idx):
    my_base = my_bases[my_base_idx]
    actions = []
    resources = [cell for cell in cells.values() if cell.resources]
    # XXX: no need for sorted now
    eggs = sorted([cell for cell in resources if cell.type == Type.EGG and cell.dist[my_base_idx] < EGG_DIST_THRES], key=lambda c: c.dist[my_base_idx])
    if len(eggs):
        target_cells = eggs
        msg = f"{len(target_cells)} EGGs: {[c.id for c in target_cells]}"
    else:
        crystals = sorted([cell for cell in resources if cell.type == Type.CRYSTAL], key=lambda c: c.dist[my_base_idx])
        target_cells = crystals[:PARALLEL_CRYSTALS]
        msg = f"{len(target_cells)} CRY {[c.id for c in target_cells]}"

    actions.append(Action.message(msg))
    for target_cell in target_cells:
        actions.append(Action.line(my_base, target_cell.id, 2))
        if target_cell.my_ants < TARGET_BOOST_MY_ANTS_THRES:
            actions.append(Action.beacon(target_cell.id, 3))
    return actions


# game loop
while True:
    for i in range(number_of_cells):
        cell = cells[i]
        resources, my_ants, opp_ants = [int(j) for j in input().split()]
        cell.resources, cell.my_ants, cell.opp_ants = resources, my_ants, opp_ants

    actions = act()
    print(";".join(actions))
