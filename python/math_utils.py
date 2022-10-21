from copy import copy


def signum(x):
    if x > 0: return 1
    if x < 0: return -1
    return 0


def gcd(a, b):
    """Greatest common divisor"""
    return _gcd_internal(abs(a), abs(b))


def _gcd_internal(a, b):
    """Greatest common divisor internal"""
    # Impl. notes: Euler algorithm, both a and b are not negative
    # There exists faster algorithm (which uses division by 2, which is faster)
    # -> Stein's algorithm https://en.wikipedia.org/wiki/Binary_GCD_algorithm
    # print a, b
    if a == b:
        return a
    if b == 1:
        return 1
    if a == 0 or b == 0:
        return max(a, b)

    return gcd(b, a % b)


def combinations_generator(n, k):
    """Generates all combinations of list of length n with k ones (lexicographically sorted).
    Storing only one indices and creating the combination list might be more performant.
    """
    combination = [1 if i >= n - k else 0 for i in range(n)]
    while True:
        yield combination
        combination = copy(combination)
        # get first one with zero before it
        one_indices = [idx for idx, value in enumerate(combination) if value]
        for one_idx_idx, one_idx in enumerate(one_indices):
            combination[one_idx] = 0
            if one_idx > 0 and one_idx - 1 != one_indices[one_idx_idx - 1]:
                for i in range(one_idx_idx + 1):
                    combination[one_idx - i - 1] = 1
                break
        else:
            # all combinations generated, breaking
            break


def is_perfect_number(n):
    """https://en.wikipedia.org/wiki/Perfect_number"""
    factors = []
    for i in range(1, n):
        if n % i == 0:
            factors.append(i)

    return sum(factors) == n


# naive brute-force algorithm
def is_prime(x):
    for i in range(2, x//2):
        if x % i == 0:
            return False
    return True


# Returns permutation indices. My naive implementation of itertools.permutations(range(n))
def permutate(n: int):
    if n < 1:
        return []
    if n == 1:
        return [[0]]

    minus_one_permutations = permutate(n - 1)
    result = []
    for perm in minus_one_permutations:
        result.extend([[*perm[:i], n-1, *perm[i:]] for i in range(len(perm), -1, -1)])
    return result

assert permutate(0) == []
assert permutate(1) == [[0]]
assert permutate(2) == [[0, 1], [1, 0]]
assert permutate(3) == [[0, 1, 2], [0, 2, 1], [2, 0, 1], [1, 0, 2], [1, 2, 0], [2, 1, 0]]
