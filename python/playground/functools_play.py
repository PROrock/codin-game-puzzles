# https://docs.python.org/3/library/functools.html

import functools


@functools.total_ordering
class Person(object):
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname

    def __gt__(self, other):
        # there should be if for not valid parameter
        return (self.firstname, self.lastname) > (other.firstname, other.lastname)

    def __eq__(self, other):
        return (self.firstname, self.lastname) == (other.firstname, other.lastname)


p1 = Person("John", "Smith")
p2 = Person("Abby", "Black")
p3 = Person("John", "Smith")
print(p1 > p2)
print(p1 < p2)
print("equal:")
print(p1 == p1)
print(p1 is p1)

print("p2")
print(p1 == p2)
print(p1 is p2)
print(p2 == p1)

print("p3")
print(p1 == p3)
print(p1 is p3)
print(p3 == p1)

print(p1 >= p3) # error w/o @functools.total_ordering
print(p1 <= p3)

print(p1)
print([p1])
