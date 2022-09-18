import sys
from collections import deque
from dataclasses import dataclass

START = "0"
EXIT = "E"


def debug(*s):
    print(*s, file=sys.stderr, flush=True)


@dataclass
class Room:
    id: str
    money: int
    left: str
    right: str


rooms_by_id = {}
n = int(input())
for i in range(n):
    id, money, next1, next2 = input().split()
    rooms_by_id[id] = Room(id, int(money), next1, next2)

# debug(exits)
max_dict = {EXIT: 0}
q = deque(START)
while len(q) and START not in max_dict:
    r = rooms_by_id[q[0]]

    options = [r.left, r.right]
    # for cycles (not present in CG test cases, but in general there can be):
    options = [o for o in options if o not in q]

    missing_rooms = [o for o in options if o not in max_dict]
    q.extendleft(missing_rooms)

    if len(missing_rooms):
        debug(f"Don't have computed both paths from room {r.id}, adding {missing_rooms=} to q")
        continue

    q.popleft()
    max_dict[r.id] = max(map(max_dict.get, options)) + r.money
    debug(f"Processed room {r.id} with sum {max_dict[r.id]}, {q=}")

print(max_dict[START])
