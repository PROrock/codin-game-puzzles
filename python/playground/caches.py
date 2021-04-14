import functools

#in 3.9
# todo revert
# @functools.cache
def fibonacci(n):
    if n <= 1:
        return 1
    return fibonacci(n-1) + fibonacci(n-2)


# for i in range(40):
#     print(fibonacci(i))


# todo "play" with @cached_property
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

p = Person()
print(p._age)
print(p.age)
print()

p.age=18
print("age set")
print(p._age)
print(p.age)
print()

del p.age
print("age deleted")
print(p._age)
print(p.age)



