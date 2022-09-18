import sys
from collections import defaultdict, deque
from dataclasses import dataclass

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

m = {}
for room in rooms_by_id.values():
    if room.has_exit():
        m[room.id] = room.money

debug(rooms_by_id)
debug(m)

q = deque(m.keys())
m[EXIT] = 0
while len(q):
    r = rooms_by_id[q.popleft()]
    nexts = [m.get(r.left), m.get(r.right)]
    if None in nexts:
        q.append(r.id)
        debug(f"Enqueuing room {r.id} once again")
        continue
    maximum = max(nexts)
    m[r.id] = maximum + r.money
    q.extend(incoming_rooms[r.id])

print(m["0"])
