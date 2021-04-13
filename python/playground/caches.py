import functools

#in 3.9
@functools.cache
def fibonacci(n):
    if n <= 1:
        return 1
    return fibonacci(n-1) + fibonacci(n-2)


for i in range(40):
    print(fibonacci(i))


# todo "play" with @cached_property
class Person:
    def __init__(self, age=0):
        self._age = age


