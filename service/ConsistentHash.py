# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : ConsistentHash.py
# Time       ：2023/3/24 22:18
# Author     ：Cheng Jungao
# version    ：python 3.9
# Description：
"""
import typing
import hashlib
from abc import abstractmethod

"""
一致性hash Node类，继承类必须实现health_check方法
"""


class Node:
    def __init__(self, url, weight=1):
        self.url = url
        self.weight = weight

    def __eq__(self, other):
        return self.url == other.url

    def __hash__(self):
        return self.url.__hash__()

    def __str__(self):
        return self.url

    @abstractmethod
    def health_check(self, response: typing.Any) -> bool:
        raise NotImplementedError


class ConsistentHash:
    def __init__(self, nodes: typing.List[Node], replicas: int = 3):
        """
        :param nodes: 节点列表
        :param replicas: 虚拟节点个数
        """
        self.replicas = replicas
        self.ring = dict()
        self.sorted_keys = []
        self.live_nodes = []
        for node in nodes:
            self.add_node(node)

    def add_node(self, node: Node):
        """
        添加节点
        :param node:
        :return:
        """
        if node in self.live_nodes:
            return
        self.live_nodes.append(node)
        for i in range(0, self.replicas * node.weight):
            key = self._hash("%s#%s" % (node.url, i))
            self.ring[key] = node
            self.sorted_keys.append(key)
        self.sorted_keys.sort()

    def remove_node(self, node: Node):
        """
        删除节点
        :param node:
        :return:
        """
        if node not in self.live_nodes:
            return
        self.live_nodes.remove(node)
        for i in range(0, self.replicas * node.weight):
            key = self._hash("%s#%s" % (node.url, i))
            del self.ring[key]
            self.sorted_keys.remove(key)

    def get_node(self, key: str):
        """
        获取节点
        :param key:
        :return:
        """
        if not self.ring:
            return None
        hash_key = self._hash(key)
        index = self._get_node_index(hash_key)
        return self.ring[self.sorted_keys[index]]

    def _hash(self, key: str):
        """
        hash函数
        :param key:
        :return:
        """
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16)

    def _get_node_index(self, hash_key):
        """
        获取节点下标
        :param hash_key:
        :return:
        """
        index = self._binary_search(hash_key)
        if index == len(self.sorted_keys):
            index = 0
        return index

    def _binary_search(self, hash_key):
        """
        二分查找
        :param hash_key:
        :return:
        """
        left = 0
        right = len(self.sorted_keys) - 1
        while left <= right:
            mid = (left + right) // 2
            if self.sorted_keys[mid] == hash_key:
                return mid
            elif self.sorted_keys[mid] < hash_key:
                left = mid + 1
            else:
                right = mid - 1
        return left

    def __str__(self):
        return str(self.ring)

    def __repr__(self):
        return str(self.ring)


