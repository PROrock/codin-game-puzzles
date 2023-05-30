from __future__ import annotations

import dataclasses
import math
import sys
from abc import ABC, abstractmethod
from collections import deque
from typing import Optional, List

from math_utils import gcd


def debug(*s):
    print(*s, file=sys.stderr, flush=True)


# todo create dataclass impl (might be faster?)
# todo consider writing a namedtuple implementation - it enables nice tricks `v[0]` and might be faster
class Point:
    """Immutable 2D point"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def l1dist(self, other_point):
        d = abs(self.x-other_point.x) + abs(self.y-other_point.y)
        # print(f"l1 dist: {self} and {other_point} is {d}", file=sys.stderr, flush=True)
        return d

    def __repr__(self):
        return f"P({self.x},{self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __bool__(self):
        return True
    def __add__(self, other_point):
        return Point((self.x + other_point.x), (self.y+other_point.y))
    def __sub__(self, other_point):
        return Point((self.x - other_point.x), (self.y-other_point.y))
    def __mul__(self, multiplier):
        return Point(self.x * multiplier, self.y * multiplier)
    # right multiplication to support 2 * p
    __rmul__ = __mul__
    def __neg__(self):
        return Point(-self.x, -self.y)
    def round(self, ndigits=None):
        return Point(round(self.x, ndigits), round(self.y, ndigits))


# todo create dataclass impl (might be faster?)
# todo consider writing a namedtuple implementation - it enables nice tricks `v[0]` and might be faster
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

    def l2_norm(self):
        """
        XXX: Consider using math.hypot(*coordinates) or math.dist(p, q), which is probably faster.
        See https://docs.python.org/3/library/math.html#math.dist
        For timing guide, see https://stackoverflow.com/a/24105845/2127340
        """
        return math.sqrt(self.x**2 + self.y**2)

    def l_inf_norm(self):
        return max(abs(self.x), abs(self.y))

    def normalize(self):
        """Normalize vector to be able to compare it with other vectors (possibly multiplies of this one)"""
        gcd_xy = gcd(self.x, self.y)
        if gcd_xy == 0 or gcd_xy == 1:
            return self
        return Vect(self.x / gcd_xy, self.y / gcd_xy)

    # this doesn't work as len must return integer not float!
    # def __len__(self):
    #     return math.sqrt(self.x**2 + self.y**2)

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


class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        self.vector = point2 - point1

    def __contains__(self, point):
        t = self._compute_t(point)
        return self._contains(point, t)

    def contains_in_line_segment(self, point):
        t = self._compute_t(point)
        return self._contains(point, t) and 0 < max(t[0], t[1]) < 1

    def _compute_t(self, point):
        return [None if self.vector.x == 0 else (point.x - self.point1.x) / float(self.vector.x),
                None if self.vector.y == 0 else (point.y - self.point1.y) / float(self.vector.y)]

    def _contains(self, point, t):
        return t[0] is None and point.x == self.point1.x \
               or t[1] is None and point.y == self.point1.y \
               or t[0] == t[1]

# todo create a Graph object? for start you can see python/medium/the-lost-files/main.py
# todo create a Tree object? potentially with search functions?
# todo create few GENERAL! algorithms/strategies like A*,MinMax,... (maybe even depth-first, breadth-first, depth-iterative-restarts, ...?)


# TODO complete this WIP
# one example of kind of implemented (not inherited) Node: see water_jug_riddle.py
@dataclasses.dataclass(frozen=True)
class Node(ABC):
    state: object
    action: object
    n_steps: int = 0
    prev_node: Optional[Node] = None

    def __repr__(self):
        return f"N({self.state}, {self.action}, {self.n_steps})"

    @abstractmethod
    def expand(self) -> List[Node]:
        pass

    @abstractmethod
    def is_goal(self) -> bool:
        pass


class Search:
    def search(self, init_state) -> Optional[Node]:
        """Breadth-first search from init_state to goal"""
        visited_states = set()
        queue = deque([self._get_start_node(init_state)])

        while queue:
            node = queue.popleft()
            if node.state not in visited_states:
                if node.is_goal():
                    self.debug(f"found solution {node}")
                    # todo or return also list of actions chronologically? so it is less dependent on implementation of Node?
                    return node

                new_nodes = node.expand()
                queue.extend(new_nodes)
                visited_states.add(node.state)

                # todo use consitent debug method!
                debug(node, new_nodes)
            else:
                debug(f"{node} already visited before!")

        self.debug("goal not reached")
        return None

    @staticmethod
    def _get_start_node(init_state) -> Node:
        return Node(None, init_state)

    @staticmethod
    def debug(*texts):
        return print(*texts, file=sys.stderr, flush=True)
