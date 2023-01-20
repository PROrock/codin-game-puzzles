import math
import re
import sys

s = input()
# c=Counter(s)
# r=[]
# for c in s:
#     r.append((count,c))


def split_to_consecutive_streaks(s):
    if not len(s):
        return []
    result = []
    substring = s[0]
    for c in s[1:]:
        if c == substring[0]:
            substring += c
        else:
            result.append(substring)
            substring = c
    result.append(substring)
    return result


n = int(input())
for i in range(n):
    m = input()
    print(m, file=sys.stderr, flush=True)
    a,b = m.split(".length()")
    letter = a[-1]
    print(a[:-1], letter,b, file=sys.stderr, flush=True)

    match = re.fullmatch("(\d+)(<=?)(\w).length\(\)(<=?)(\d+)", m)
    # print(match.groups(), file=sys.stderr, flush=True)
    lb,lo,letter,uo,ub = match.groups()
    lb=int(lb)
    ub=int(ub)
    if "=" in lo:
        lb-=1
    if "=" in uo:
        ub+=1

    bs = split_to_consecutive_streaks(s)
    print(lb,ub, file=sys.stderr, flush=True)
    print(bs, file=sys.stderr, flush=True)

    solution = 0
    for ss in bs:
        if ss[0] == letter and lb<len(ss)<ub:
            solution+=1

    print(solution)
