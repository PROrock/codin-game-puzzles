from __future__ import annotations

import dataclasses
import sys
from collections import deque
from typing import Optional, List, Tuple


def debug(*s):
    print(*s, file=sys.stderr, flush=True)


target = int(input())
containers_count = int(input())
containers = []
for i in range(containers_count):
    containers.append(int(input()))

debug(target)
debug(containers)

init_state = tuple([0]*containers_count)


@dataclasses.dataclass(frozen=True)
class Node:
    action: object
    state: Tuple[int]
    n_steps: int = 0
    prev_node: Optional[Node] = None

    def __repr__(self):
        return f"N({self.state}, {self.action}, {self.n_steps})"

    def expand(self) -> List[Node]:
        expanded = []

        # "Pour" water from a container to another. No water is spilled with this move.
        for source in range(containers_count):
            if self.state[source] == 0:
                continue

            for target in range(containers_count):
                if target == source or self.state[target] == containers[target]:
                    continue

                poured = min(containers[target]-self.state[target], self.state[source])
                new_state = list(self.state)
                new_state[source] -= poured
                new_state[target] += poured
                expanded.append(Node("pour", tuple(new_state), self.n_steps + 1, prev_node=self))

        # "Empty" water from a container to empty it completely
        for source in range(containers_count):
            if self.state[source] == 0:
                continue

            new_state = list(self.state)
            new_state[source] = 0
            expanded.append(Node("empty", tuple(new_state), self.n_steps + 1, prev_node=self))

        # "Fill" a container to reach its capacity
        for target in range(containers_count):
            if self.state[target] == containers[target]:
                continue

            new_state = list(self.state)
            new_state[target] = containers[target]
            expanded.append(Node("fill", tuple(new_state), self.n_steps + 1, prev_node=self))

        return expanded

    def is_goal(self) -> bool:
        return target in self.state


class Search:
    def search(self, init_state) -> Optional[Node]:
        visited_states = set()
        queue = deque([self._get_start_node(init_state)])

        while queue:
            node = queue.popleft()
            if node.state not in visited_states:
                if node.is_goal():
                    self.debug(f"found solution {node}")
                    return node

                new_nodes = node.expand()
                queue.extend(new_nodes)
                visited_states |= {node.state}

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


goal_node = Search().search(init_state)
print(goal_node.n_steps)
