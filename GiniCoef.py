import numba as nb
from numpy import cumsum, insert

# # nb.jit(nopython=True) is a shortcut for @nb.njit()
# @nb.njit()
def Gini(values):

    n = len(values)
    assert(n > 0), 'Empty list of values'
    sorted_Values = sorted(values)              # Sort smallest to largest

    # Alternative 0 [SLOW]
    # Find cumulative totals
    # cumm = [0]
    # for i in range(n):
    #     cumm.append(sum(sorted_Values[0: (i + 1)]))

    # Alternative 1 [FASTER]
    cumm = cumsum(sorted_Values)
    cumm = insert(cumm, 0, 0)

    # Calculate Lorenz points
    LorenzPoints = [[], []]
    sumYs = 0                                   # Some of all y values
    for i in range(1, n + 2):
        x = 100.0 * (i - 1) / n
        y = 100.0 * (cumm[i - 1] / float(cumm[n]))
        LorenzPoints[0].append(x)
        LorenzPoints[1].append(y)
        sumYs += y

    gini_Coef = 100 + (100 - 2 * sumYs) / n     # Gini index

    return [gini_Coef/100, LorenzPoints]


