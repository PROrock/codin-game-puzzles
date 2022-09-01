# from https://stackoverflow.com/a/28037067/2127340

import timeit
setup = 'from __main__ import foo_dict, foo_list'

N = 7
l = list(str(i) for i in range(N))
d = dict((str(i), i) for i in range(N))
def foo_dict(k):
    return d[k]
def foo_list(k):
    return l.index(k)

print(timeit.repeat('[foo_dict(str(i)) for i in range(7)]', setup))
print(timeit.repeat('[foo_list(str(i)) for i in range(7)]', setup))

print(timeit.repeat('foo_dict("6")', setup))
print(timeit.repeat('foo_list("6")', setup))
