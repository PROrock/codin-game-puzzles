# https://docs.python.org/3/howto/sorting.html#sortinghowto
from operator import itemgetter, attrgetter, methodcaller
from typing import NamedTuple, Tuple

node_tuples = [
    # position, history/n. of moves, last action
    ((2,1), 0, "attack"),
    ((5,5), 3, "teleport"),
    ((2,0), 1, "move"),
    ((2,2), 1, "defend"),
]

def tuple_test():
    print(node_tuples)
    print(sorted(node_tuples))
    # node_tuples.sort()
    # print(node_tuples)

    print(sorted(node_tuples, key=lambda n:n[1]))  # sort by history
    print(sorted(node_tuples, key=itemgetter(1)))  # sort by history
    print("double sort:")
    print(sorted(node_tuples, key=itemgetter(1, 2)))  # sort by history, then action name


# Node = namedtuple("Node", "position history last_action")
class Node(NamedTuple):
    position: Tuple[int]
    history: int
    last_action: str

    def h(self):
        return self.history*-1

node_named = list(map(Node._make, node_tuples))
# node_named = list(map(Node.__init__, node_tuples))  # not like this
# node_named = list(map(lambda t: Node(*t), node_tuples))

# node_named = [
#     # position, history/n. of moves, last action
#     Node((2,1), 0, "attack"),
#     Node((5,5), 3, "teleport"),
#     Node((2,0), 1, "move"),
#     Node((2,2), 1, "defend"),
# ]

print(node_named)
print(sorted(node_named))

print(sorted(node_named, key=lambda n:n[1]))  # sort by history
print(sorted(node_named, key=itemgetter(1)))  # sort by history
print(sorted(node_named, key=lambda n:n.history))  # sort by history, has reference to the field!
print(sorted(node_named, key=attrgetter("history")))  # sort by history
print("double sort:")
print(sorted(node_named, key=itemgetter(1, 2)))  # sort by history, then action name
print(sorted(node_named, key=attrgetter("history", "last_action")))  # sort by history, then action name

print(sorted(node_named, key=methodcaller("h")))  # sort by .h() call

