# https://docs.python.org/3/library/itertools.html
import functools

import itertools as it

all_ones = it.repeat(1)
print(next(all_ones))
print(next(all_ones))
print(next(all_ones))
# raises err
# print(len(all_ones))


squares = [x*x for x in range(10)]
print(squares)

squares2 = list(map(pow, range(10), it.repeat(2)))
# instead of
# squares2 = list(map(pow, range(10), [2 for _ in range(10)]))
# or
# squares2 = list(map(lambda x: pow(x,2), range(10)))
print(squares2)

# infinite loop
# print(list(it.repeat(1)))
print(list(it.repeat(1, times=2)))

#----------------

alternatig_ones = it.cycle((1, -1))
print(next(alternatig_ones), next(alternatig_ones))
print(next(alternatig_ones), next(alternatig_ones))
print(next(alternatig_ones), next(alternatig_ones))

#---------------

print(list(it.permutations("abc")))

print(list(it.permutations("abc", r=2)))
print(list(it.permutations("cab", r=2)))
print(list(it.combinations("cab", r=2)))
print(list(it.combinations_with_replacement("cab", r=2)))

s = "abc"
power_set = functools.reduce(lambda a,b: a+b, [list(it.combinations(s, r=i)) for i in range(len(s)+1)])
print("Power set", power_set)

a="abc"
b="123"
zipped = list(zip(a,b))
print(zipped)

# unzip via zip
aaa, bbb = zip(*zipped)
print(aaa, bbb)

# tee duplicates the original iterable!
aa, bb = it.tee(zipped, 2)
print(aa, bb)
print(list(aa), list(bb))
