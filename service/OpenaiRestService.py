# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : OpenaiRestService.py
# Time       ：2023/3/24 23:22
# Author     ：Cheng Jungao
# version    ：python 3.9
# Description：
"""
import typing

from config.ServiceConfig import configuration
from model import Params
from service.ConsistentHash import Node
from service.RestServiceDao import RestServiceDao


class OpenaiServiceNode(Node):

    def health_check(self, response: typing.Any) -> bool:
        pass


class OpenaiRestService(RestServiceDao):
    def __init__(self):
        nodes = []
        for node in configuration.openaiConfig.get("nodes"):
            nodes.append(OpenaiServiceNode(node.get("url"), node.get("weight")))
        self.token = configuration.openaiConfig.get("token")
        super().__init__(nodes, configuration.openaiConfig.get("timeout"),
                         configuration.openaiConfig.get("keep_alive_timeout"),
                         configuration.openaiConfig.get("max_connections"),
                         configuration.openaiConfig.get("max_keep_alive_connections"),
                         configuration.openaiConfig.get("ping_path"),
                         configuration.openaiConfig.get("proxy"))

    def get_request_key(self, path: str, params: dict = None, headers: dict = None) -> str:
        return params.__str__()

    def completions(self, params: Params) -> typing.Any:
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": params.prompt}],
            "temperature": 0.7
        }
        headers = {"accept": "application/json", "content-type": "application/json",
                   "authorization": "Bearer " + self.token}
        return self.post("/v1/chat/completions", data=data, headers=headers)
