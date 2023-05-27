import enum
import sys
from dataclasses import dataclass
from enum import Enum


def debug(*s):
    print(*s, file=sys.stderr, flush=True)


@enum.unique
class Type(Enum):
    EMPTY = 0
    EGG = 1
    CRYSTAL = 2


@dataclass(frozen=True)
class Cell:
    id: int
    type: Type
    init_resources: int
    neighs: tuple


@dataclass(frozen=True)
class CellState:
    id: int
    resources: int
    my_ants: int
    opp_ants: int
    cell: Cell


cells = {}

number_of_cells = int(input())  # amount of hexagonal cells in this map
for i in range(number_of_cells):
    # _type: 0 for empty, 1 for eggs, 2 for crystal
    # initial_resources: the initial amount of eggs/crystals on this cell
    # neigh_0: the index of the neighbouring cell for each direction
    _type, initial_resources, neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5 = [int(j) for j in input().split()]
    cells[i] = Cell(i, Type(_type), initial_resources, tuple())
number_of_bases = int(input())
my_bases = [int(i) for i in input().split()]
opp_bases = [int(i) for i in input().split()]
# debug(f"{my_bases=}")
# debug(f"{opp_bases=}")

# game loop
while True:
    cell_states = {}
    for i in range(number_of_cells):
        # resources: the current amount of eggs/crystals on this cell
        # my_ants: the amount of your ants on this cell
        # opp_ants: the amount of opponent ants on this cell
        resources, my_ants, opp_ants = [int(j) for j in input().split()]
        cell_states[i] = CellState(i, resources, my_ants, opp_ants, cells[i])

    my_base = my_bases[0]
    crystals = [cell_state for cell_state in cell_states.values() if cell_state.resources and cell_state.cell.type == Type.CRYSTAL]
    crystal_state = max(crystals, key=lambda state: state.resources)
    print(f"LINE {my_base} {crystal_state.id} {1}")

    # WAIT | LINE <sourceIdx> <targetIdx> <strength> | BEACON <cellIdx> <strength> | MESSAGE <text>
    # print("WAIT")
