def signum(x):
    if x > 0: return 1
    if x < 0: return -1
    return 0


# copy of Python 3.5 implementation - probably not needed
def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


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
    combination = [1 if i >= n - k else 0 for i in xrange(n)]
    while True:
        yield combination
        combination = copy(combination)
        # get first one with zero before it
        one_indices = [idx for idx, value in enumerate(combination) if value]
        for one_idx_idx, one_idx in enumerate(one_indices):
            combination[one_idx] = 0
            if one_idx > 0 and one_idx - 1 != one_indices[one_idx_idx - 1]:
                for i in xrange(one_idx_idx + 1):
                    combination[one_idx - i - 1] = 1
                break
        else:
            # all combinations generated, breaking
            break
