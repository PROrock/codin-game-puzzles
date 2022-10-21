from itertools import permutations

def solve(l):
    perms = permutations(l)
    min_len = None
    for perm in perms:
        length = compute_one_order(perm)
        if min_len is None or length < min_len:
            min_len = length
    return min_len

def compute_one_order(l):
    s = ""
    for subseq in l:
        s = concat(s, subseq)
    return len(s)

def concat(a, b):
    if b in a:
        return a
    for i in range(min(len(a), len(b)), 0, -1):
        if a.endswith(b[:i]):
            return a + b[i:]
    return a+b

n = int(input())
l = [input() for _ in range(n)]
print(solve(l))

##################################
assert concat("aa", "a") == "aa"
assert concat("ac", "a") == "ac"
assert concat("ac", "g") == "acg"
assert concat("ac", "ca") == "aca"
assert concat("aca", "ca") == "aca"
assert concat("acaca", "cag") == "acacag"
assert concat("acaca", "att") == "acacatt"
assert solve(["att", "acaca"]) == "acacatt"
assert solve(["acaca", "att", "cat"]) == "acacatt"
