import sys
from collections import defaultdict, deque
from dataclasses import dataclass

START = "0"
EXIT = "E"


def debug(*s):
    print(*s, file=sys.stderr, flush=True)


@dataclass(frozen=True)
class Room:
    id: str
    money: int
    left: str
    right: str

    def get_next_rooms(self):
        return [self.left, self.right]

    def has_exit(self):
        return EXIT in self.get_next_rooms()


rooms_by_id = {}
incoming_rooms = defaultdict(list)
n = int(input())
for i in range(n):
    id, money, next1, next2 = input().split()
    rooms_by_id[id] = Room(id, int(money), next1, next2)
    if next1 != EXIT:
        incoming_rooms[next1].append(id)
    if next2 != EXIT:
        incoming_rooms[next2].append(id)

exits = []
for room in rooms_by_id.values():
    if room.has_exit():
        exits.append(room.id)

# debug(rooms_by_id)
# debug(exits)


def build_max_dict(exit):
    m = {EXIT: 0, exit: rooms_by_id[exit].money}
    q = deque(incoming_rooms[exit])
    visited = set()
    while len(q) and START not in m:
        r = rooms_by_id[q.popleft()]
        nexts = [m.get(r.left), m.get(r.right)]
        if None in nexts:
            debug(f"Enqueuing room {r.id} once again. {m=}")
            if r.left not in m:
                q.appendleft(r.left)
            if r.right not in m:
                q.appendleft(r.right)
            q.append(r.id)
            continue
        maximum = max(nexts)
        m[r.id] = maximum + r.money
        visited.add(r.id)

        incoming = [id for id in incoming_rooms[r.id] if id not in visited]
        debug(f"Processed room {r.id} with sum {m[r.id]}, next processing: {incoming}")
        q.extend(incoming)
    return m


max_per_exit = []
for e in exits:
    max_dict = build_max_dict(e)
    max_per_exit.append(max_dict[START])

print(max(max_per_exit))
