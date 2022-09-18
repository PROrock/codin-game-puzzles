import sys


def debug(*s):
    print(*s, file=sys.stderr, flush=True)

r = {}
n = int(input())
for i in range(n):
    room = input().split()
    id, money, netx1, next2 = room
    id = int(id)
    money = int(money)
    r[id] = (id, money, netx1, next2)

# Write an answer using print
# To debug: print("Debug messages...", file=sys.stderr, flush=True)


print(r[0][1])
