# my made task: find top 3 most frequent words in paragraph
import string
from collections import Counter


def top3(string: str):
    splitted = string.split()
    c = Counter(splitted)
    return c.most_common(3)

s="""

I wanna be the very best
Like no one ever was
To catch them is my real test
To train them is my cause

I will travel across the land
Searching far and wide
Each Pokemon to understand
The power that's inside

(Pokemon, gotta catch 'em all)
Its you and me
I know it's my destiny
(Pokemon)
Oh, you're my best friend
In a world we must defend
(Pokemon, gotta catch 'em all)
A heart so true
Our courage will pull us through

You teach me and I'll teach you
Pokemon
(gotta catch 'em all)
Gotta catch 'em all
(Pokemon)
"""
top = top3(s)
print(top)


# -------
# collections.deque
# constant time to add elem to either front or back!
# bounded (with max size) useful to mimic tail in linux - if only last 10 rows/items are interesting

from collections import deque

class Q(object):
    def __init__(self):
        self.q = deque()
    def new(self, customer):
        self.q.append(customer)
    def serve(self):
        name = self.q.popleft()
        print(f"Served {name}")
    def new_vip(self, vip):
        self.q.appendleft(vip)
    def __repr__(self):
        return f"Q({list(self.q)})"

q = Q()
q.new("Ondra")
q.new("Hanka")
q.serve()
print(q)
q.new_vip("borec")
q.serve()
q.serve()

# ----------
print(string.ascii_letters)
print(string.digits)







