import random


def random_list(n, a, b):
    return [random.randint(a, b) for _ in range(n)]

# print(random_list(5, 0, 20))
# print()

print("100000")
print("0") # transport lines
print("0") # pods
n = 126
print(n)
for i in range(n):
    type_ = random.randint(0, 20)
    astronauts = " ".join([str(x) for x in random_list(random.randint(1, 20), 1, 20)]) if type_ == 0 else ""
    print(type_, i, random.randint(0, 159), random.randint(0, 89), astronauts)
