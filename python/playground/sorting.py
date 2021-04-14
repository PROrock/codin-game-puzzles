# https://docs.python.org/3/howto/sorting.html#sortinghowto
from operator import itemgetter

node_tuples = [
    # position, history/n. of moves, last action
    ((2,1), 0, "attack"),
    ((5,5), 3, "teleport"),
    ((2,0), 1, "move"),
    ((2,2), 1, "defend"),
]

# todo named tuple and use attrgetter
node_tuples = [
    # position, history/n. of moves, last action
    ((2,1), 0, "attack"),
    ((5,5), 3, "teleport"),
    ((2,0), 1, "move"),
    ((2,2), 1, "defend"),
]


print(node_tuples)
print(sorted(node_tuples))
# node_tuples.sort()
# print(node_tuples)

print(sorted(node_tuples, key=lambda n:n[1]))  # sort by history
print(sorted(node_tuples, key=itemgetter(1)))  # sort by history
print(sorted(node_tuples, key=itemgetter(1, 2)))  # sort by history, then action name


