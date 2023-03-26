# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : RestServiceDao.py
# Time       ：2023/3/24 22:47
# Author     ：Cheng Jungao
# version    ：python 3.9
# Description：
"""
import threading
import time
from abc import abstractmethod
from typing import List

import httpx
from httpx import Timeout, Limits

from service.ConsistentHash import ConsistentHash, Node


class HealthCheckThread(threading.Thread):
    def __init__(self, nodes: List[Node], client: httpx.Client, ping_path: str,
                 consistent_hash:ConsistentHash, interval=60):
        super().__init__()
        self.nodes = nodes
        self.interval = interval
        self._stop_event = threading.Event()
        self.client = client
        self.ping_path = ping_path
        self.consistent_hash = consistent_hash

    def stop(self):
        self._stop_event.set()

    def run(self):
        while not self._stop_event.is_set():
            for node in self.nodes:
                try:
                    response = self.client.get(node.url + self.ping_path)
                    if node.health_check(response):
                        self.consistent_hash.add_node(node)
                    else:
                        self.consistent_hash.remove_node(node)
                except Exception as e:
                    print(f"health check failed: {e}")
                    self.consistent_hash.remove_node(node)
            time.sleep(self.interval)


class RestServiceDao:
    def __init__(self, nodes: List[Node], timeout=5, keep_alive_connections=5,
                 keepalive_expiry=60, max_connections=10, ping_path=None, proxy=None):
        self.client = httpx.Client(
            timeout=Timeout(timeout, connect=timeout, read=timeout),
            limits=Limits(max_connections=max_connections,
                          max_keepalive_connections=keep_alive_connections,
                          keepalive_expiry=keepalive_expiry),
            proxies=proxy
        )
        self.consistent_hash = ConsistentHash(nodes)
        if ping_path is not None:
            self.health_check_thread = HealthCheckThread(nodes, self.client, ping_path, self.consistent_hash)
            self.health_check_thread.setDaemon(True)
            self.health_check_thread.start()

    def get(self, path: str, params: dict = None, headers: dict = None) -> dict:
        url = self.consistent_hash.get_node(self.get_request_key(path=path, params=params, headers=headers)).url + path
        return self.client.get(url, params=params, headers=headers).json()

    def post(self, path: str, data: dict = None, headers: dict = None) -> dict:
        url = self.consistent_hash.get_node(self.get_request_key(path=path, params=data, headers=headers)).url + path
        return self.client.post(url, json=data, headers=headers).json()

    @abstractmethod
    def get_request_key(self, path: str, params: dict = None, headers: dict = None) -> str:
        raise NotImplementedError

    def close(self):
        self.client.close()
        if self.health_check_thread is not None:
            self.health_check_thread.stop()
