#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Similar to the knapscak problem, but subject to total included items <= k <= n.

Algorithm: (Dynamic programming)
Denote S to be the optimal solution, and item-n to be the last item.
Consider whether item-n is in S:
1. item-n is NOT in S:
   => S must be optimal among only the first (n - 1) items with budget k and
      capacity W.
   => S = the optimal solution among only the first (n - 1) items with budget k
          and capacity W
2. item-n is in S:
   => S must be optimal among only the first (n - 1) items with budget (k - 1)
      and capacity (W - w_n).
   => S = the optimal solution among only the first (n - 1) items with budget
      (k - 1) and capacity (W - w_n) + v_n

i.e.,
Let S(i, b, x) be the optimal solution for the subproblem among the first i
items with budget b and capacity x, then
S(i, b, x) = max{S(i - 1, b, x), S(i - 1, b - 1, x - w_i) + v_i}
"""

__author__ = 'Ziang Lu'

from typing import List, Set


def knapsack_with_budget(vals: List[float], weights: List[int], budget: int,
                         cap: int) -> Set[int]:
    """
    Solves the knapsack problem (with budget) of the items with the given values
    and weights, with the given budget and capacity, in an bottom-up way.
    :param vals: list[float]
    :param weights: list[int]
    :param budget: int
    :param cap: int
    :return: set{int}
    """
    # Check whether the input arrays are None or empty
    if not vals:
        return set()
    # Check whether the input budget is non-negative
    if budget < 0:
        return set()
    # Check whether the input capacity is non-negative
    if cap < 0:
        raise set()

    n = len(vals)
    # Initialization
    subproblems = [
        [[0.0] * (cap + 1) for _ in range(budget + 1)]
        for _ in range(n)
    ]
    for b in range(budget + 1):
        for x in range(cap + 1):
            if b >= 1 and weights[0] <= x:
                subproblems[0][b][x] = vals[0]
    # Bottom-up calculation
    for item in range(1, n):
        for b in range(budget + 1):
            for x in range(cap + 1):
                if b <= 0 or weights[item] > x:
                    subproblems[item][b][x] = subproblems[item - 1][b][x]
                else:
                    result_without_curr = subproblems[item - 1][b][x]
                    result_with_curr = \
                        subproblems[item - 1][b - 1][x - weights[item]] + \
                        vals[item]
                    subproblems[item][b][x] = max(result_without_curr,
                                                  result_with_curr)
    return _reconstruct(vals, weights, budget, cap, subproblems)
    # Overall running time complexity: O(n*k*W), where k is the budget and W is
    # the knapsack capacity


def _reconstruct(vals: List[float], weights: List[int], budget: int, cap: int,
                 dp: List[List[List[float]]]) -> Set[int]:
    """
    Private helper function to reconstruct the included items according to the
    optimal solution using backtracking.
    :param vals: list[float]
    :param weights: list[int]
    :param budget: int
    :param cap: int
    :param dp: list[list[list[float]]]
    :return: set{int}
    """
    included = set()
    item, curr_budget, curr_cap = len(vals) - 1, budget, cap
    while item >= 1:
        result_without_curr = dp[item - 1][curr_budget][curr_cap]
        if curr_budget >= 1 and weights[item] <= curr_cap and \
                result_without_curr < \
                dp[item - 1][curr_budget - 1][curr_cap - weights[item]] + \
                vals[item]:
            included.add(item)
            curr_budget -= 1
            curr_cap -= weights[item]
        item -= 1
    if curr_budget >= 1 and weights[0] <= curr_cap:
        included.add(0)
    return included
    # Running time complexity: O(n)
