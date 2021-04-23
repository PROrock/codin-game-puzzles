import collections
from dataclasses import dataclass
from typing import NamedTuple


class Employee(NamedTuple):
    name: str
    id: int
# This is equivalent to:

Employee2 = collections.namedtuple('Employee2', ['name', 'id'])

e1 = Employee("ondra", 1)
print(e1)
print(e1[1])

# e2 = Employee2("ondra")  # error, missing id!
e2 = Employee2("ondra", 1)
print(e2)
print(e2[0])

@dataclass
class EmployeeData:
    """doc string available"""
    name: str
    id: int

ed = EmployeeData("ondra", 1)
print(ed)
# print(ed[1])  #error!
print(ed.id)


from types import SimpleNamespace

edd = SimpleNamespace(firstname="Edgar", lastname="Wright")
print(edd.firstname)  # no IDE help here :-(
print(edd.lastname)
print(edd)
print([edd])

@dataclass
class Person:
    firstname: str
    lastname: str

p = Person("Edgar", lastname="Wright")
print(p.firstname)  #IDE help here :-)
print(p.lastname)
print(p)
print([p])
