#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Given an array, find the k-th largest element.

Naive implementation:
1. Sort the array
2. Take out the k-th largest element
O(nlog n)
"""

__author__ = 'Ziang Lu'

import random


def kth_largest(nums, k):
    """
    Finds the k-th largest element in the given array.
    :param nums: list[int]
    :param k: int
    :return: int
    """
    # Check whether the input array is null or empty
    if nums is None or len(nums) == 0:
        return 0
    # Check whether the input k is valid
    if k < 0 or k >= len(nums):
        return 0

    return _kth_largest_helper(nums, left=0, right=len(nums) - 1, k=k)
    # Overall running time complexity: O(n), better than O(nlog n)


def _kth_largest_helper(nums, left, right, k):
    """
    Private helper function to find the k-th largest element in the given array
    recursively.
    :param nums: list[int]
    :param left: int
    :param right: int
    :param k: int
    :return: int
    """
    # Base case 1: Shrink to only one number
    if left == right:
        return nums[left]
    # Choose a pivot from the given sub-array, and move it to the left
    _choose_pivot(nums, left=left, right=right)
    pivot_idx = _partition(nums, left=left, right=right)
    # Base case 2: Found it
    if pivot_idx == k:
        return nums[pivot_idx]

    # Recursive case
    if pivot_idx > k:
        return _kth_largest_helper(nums, left=left, right=pivot_idx, k=k)
    else:
        return _kth_largest_helper(nums, left=pivot_idx + 1, right=right, k=k)


def _choose_pivot(nums, left, right):
    """
    Helper function to choose a pivot from the given sub-array, and move it to
    the left.
    :param nums: list[int]
    :param left: int
    :param right: int
    :return: None
    """
    # [Randomized] Randomly choose a pivot from the given sub-array
    pivot_idx = random.randrange(left, right + 1)
    # Move the pivot to the left
    if pivot_idx != left:
        nums[left], nums[pivot_idx] = nums[pivot_idx], nums[left]


def _partition(nums, left, right):
    """
    Helper function to partition the given sub-array.
    :param nums: list[int]
    :param left: int
    :param right: int
    :return: int
    """
    # The pivot has already been moved to the left.
    pivot = nums[left]

    # Iterate over the sub-array, use a pointer to keep track of the smaller
    # part, and swap the current number with the pointer as necessary
    smaller_ptr = left + 1
    i = left + 1
    while True:
        while i <= right and nums[i] > pivot:
            i += 1
        if i > right:
            break
        if i != smaller_ptr:
            nums[smaller_ptr], nums[i] = nums[i], nums[smaller_ptr]
        smaller_ptr += 1
        i += 1
    if left != smaller_ptr - 1:
        nums[left], nums[smaller_ptr - 1] = nums[smaller_ptr - 1], nums[left]
    return smaller_ptr - 1
