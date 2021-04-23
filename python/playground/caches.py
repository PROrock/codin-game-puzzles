import functools

# from 3.9
# @functools.cache
# from 3.2
# @functools.lru_cache
def fibonacci(n):
    # if n <= 1:
    #     return 1
    # or
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)


# for i in range(40):
#     print(fibonacci(i))
#
# print(fibonacci.cache_info())
# print(fibonacci.cache_clear())
# print(fibonacci.__wrapped__(1))  # bypass of the cache
# print(fibonacci.cache_info())


class Person:
    def __init__(self, age=0):
        self._age = age

    # @property
    # @functools.cache  # funguje a ma to i setter
    @functools.cached_property # nemuze to mit setter asi a cached_property allows writes
    # v podstate je to lazy-init
    def age(self):
        return fibonacci(34)

    # @age.setter
    # def age(self, val):
    #     print("nekdo se snazi nasetovat age!")
    #     self._age = val


# p = Person()
# print(p._age)
# print(p.age)
# print()
#
# p.age=18
# print("age set")
# print(p._age)
# print(p.age)
# print()
#
# del p.age
# print("age deleted")
# print(p._age)
# print(p.age)
