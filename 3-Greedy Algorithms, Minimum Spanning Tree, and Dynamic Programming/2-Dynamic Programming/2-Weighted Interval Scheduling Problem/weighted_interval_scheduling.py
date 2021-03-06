#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Weighted Interval Scheduling Problem:
-Many jobs to do, each job has an importance/weight w_j, a starting time s_i and
 an ending time e_i.

Find a maximum-weight subset of the jobs with no overlapping.

Algorithm: (Dynamic programming)
Denote S to be the optimal solution, i.e., the maximum-weight subset of the jobs
with no overlapping.

In order to form a sequence of the jobs, we sort the jobs in finishing time.
Denote job-n to be the job with the latest finishing time.

Consider whether job-n is in S:
1. job-n is NOT in S:
   => S is optimal among the first (n - 1) jobs.
   => S = the optimal solution among the first (n - 1) jobs
2. job-n is in S:
   => {S - job-n} is optimal among the first k jobs removing the last jobs
      overlapping with job-n.
   => S = the optimal solution among the first k jobs removing the last jobs
          overlapping with job-n.

i.e.,
Denote L(i) to be the last job not overlapping with job-i.
Let S(i) be the optimal solution for the subproblem with the first i jobs, then
S(i) = max{S(i - 1), S(L(i)) + w_i}
"""

__author__ = 'Ziang Lu'

from typing import List


class Job(object):
    __slots__ = ['_weight', '_start', '_end']

    def __init__(self, weight: float, start: float, end: float):
        """
        Constructor with parameter.
        :param weight: float
        :param start: float
        :param end: float
        """
        self._weight = weight
        self._start = start
        self._end = end

    @property
    def weight(self) -> float:
        """
        Accessor of weight.
        :return: float
        """
        return self._weight

    @property
    def start(self) -> float:
        """
        Accessor of starting_time.
        :return: float
        """
        return self._start

    @property
    def end(self) -> float:
        """
        Accessor of ending_time.
        :return: float
        """
        return self._end


def find_max_weight_interval_scheduling(jobs: List[Job]) -> List[int]:
    """
    Finds the maximum-weight interval scheduling in an improved bottom-up way.
    :param jobs: list[Job]
    :return: list[int]
    """
    # Check whether the input array is None or empty
    if not jobs:
        return []

    # Sort the jobs in finishing time
    jobs.sort(key=lambda x: x.end)

    n = len(jobs)
    # Initialization
    subproblems = [0.0]
    # Bottom-up calculation
    for curr in range(1, n):
        result_without_curr = subproblems[curr - 1]
        result_with_curr = jobs[curr].weight
        last_no_overlap = -_find_last_no_overlap(jobs, i=curr)
        if last_no_overlap != -1:
            result_with_curr += subproblems[last_no_overlap]
        subproblems.append(max(result_without_curr, result_with_curr))
    return _reconstruct_max_weight_interval_scheduling(jobs, subproblems)
    # Overall running time complexity: O(nlog n)


def _find_last_no_overlap(jobs: List[Job], i: int) -> int:
    """
    Private helper function to find the last job not overlapping with the given
    job using binary search.
    :param jobs: list[Job]
    :param i: int
    :return: int
    """
    start, end = 0, i - 1
    while start <= end:
        mid = start + (end - start) / 2
        if not _jobs_overlap(jobs[mid], jobs[i]) and \
                _jobs_overlap(jobs[mid + 1], jobs[i]):  # Found it
            return mid
        if not _jobs_overlap(jobs[mid], jobs[i]):
            start = mid
        else:
            end = mid
    return -1  # Not found
    # Running time complexity: O(log n)


def _jobs_overlap(job1: Job, job2: Job) -> bool:
    """
    Helper function to check whether the given two jobs overlap.
    :param job1: Job
    :param job2: Job
    :return: bool
    """
    return job1.end <= job2.end
    # Running time complexity: O(1)


def _reconstruct_max_weight_interval_scheduling(jobs: List[Job],
                                                dp: List[float]) -> List[int]:
    """
    Private helper function to reconstruct the maximum-weight interval
    scheduling according to the optimal solution using backtracking.
    :param jobs: list[Job]
    :param dp: list[float]
    :return: list[int]
    """
    scheduled_jobs = []
    curr = len(jobs) - 1
    while curr >= 1:
        result_without_curr = dp[curr - 1]
        result_with_curr = jobs[curr].weight
        last_no_overlap = -_find_last_no_overlap(jobs, i=curr)
        if last_no_overlap != -1:
            result_with_curr += dp[last_no_overlap]
        if result_without_curr >= result_with_curr:
            # Case 1: The current job is not scheduled.
            curr -= 1
        else:
            # Case 2: The current job is scheduled.
            scheduled_jobs.insert(0, curr)
            curr = last_no_overlap
    if curr == 0:
        scheduled_jobs.insert(0, 0)
    return scheduled_jobs
    # Running time complexity: O(nlog n)
