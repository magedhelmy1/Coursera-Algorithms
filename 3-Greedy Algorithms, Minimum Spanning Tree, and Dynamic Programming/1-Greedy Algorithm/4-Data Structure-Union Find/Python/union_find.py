#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Eager Union implementation of Union-Find data structure.
Maintain a partition of a set of objects
=> Maintain a linked structure, and each subset has an arbitrary leader
   (representative of the group) object, and the group name is exactly the name
   of the leader.
"""

__author__ = 'Ziang Lu'

from typing import List


class IllegalArgumentError(ValueError):
    pass


class UnionFindObj(object):
    __slots__ = ['_leader']

    def __init__(self):
        """
        Default constructor.
        """
        self._leader = self

    @property
    def leader(self):
        """
        Accessor of leader.
        :return: UnionFindObj
        """
        return self._leader

    @leader.setter
    def leader(self, leader) -> None:
        """
        Mutator of leader.
        :param leader: UnionFindObj
        :return: None
        """
        self._leader = leader

    @property
    def obj_name(self) -> str:
        """
        Returns the name of this object.
        :return: str
        """
        pass


class UnionFind(object):
    __slots__ = ['_groups']

    @staticmethod
    def _update_leader(group: List[UnionFindObj],
                       new_leader: UnionFindObj) -> None:
        """
        Private helper function to update the leader of the given group to the
        given new leader.
        :param group: list[UnionFindObj]
        :param new_leader: UnionFindObj
        :return: None
        """
        for obj in group:
            obj.leader = new_leader
        # Running time complexity: O(1)

    def __init__(self, objs: List[UnionFindObj]):
        """
        Constructor with parameter.
        :param objs: list[UnionFindObj]
        """
        self._groups = {}
        for obj in objs:
            self._groups[obj.obj_name] = [obj]

    def num_of_groups(self) -> int:
        """
        Returns the number of groups.
        :return: int
        """
        return len(self._groups)

    def find(self, obj: UnionFindObj) -> str:
        """
        Returns the name of the group, which is exactly the name of the group
        leader that the given object belongs to.
        :param obj: UnionFindObj
        :return: str
        """
        return obj.leader.obj_name
        # Running time complexity: O(1)

    def union(self, name_a: str, name_b: str) -> None:
        """
        Fuses the given two groups together.
        Objects in the first group and objects in the second group should all
        coalesce, and be now in one single group.
        :param name_a: str
        :param name_b: str
        :return: None
        """
        # Check whether the input strings are null or empty
        if not name_a or not name_b:
            raise IllegalArgumentError(
                'The input group names should not be None or empty.'
            )
        # Check whether the input group names exist
        if name_a not in self._groups or name_b not in self._groups:
            raise IllegalArgumentError(
                "The input group names don't both exist."
            )

        group_a, group_b = self._groups[name_a], self._groups[name_b]
        # In order to reduce the number of leader updates, let the smaller group
        # inherit the leader of the larger one.
        if len(group_a) >= len(group_b):
            larger, smaller = group_a, group_b
        else:
            larger, smaller = group_b, group_a
        larger_leader = larger[0].leader
        smaller_name = smaller[0].leader.obj_name
        self._update_leader(group=smaller, new_leader=larger_leader)

        larger.extend(smaller)
        self._groups[larger_leader.obj_name] = larger
        self._groups.pop(smaller_name)
