# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : ServiceConfig.py
# Time       ：2023/3/24 22:46
# Author     ：Cheng Jungao
# version    ：python 3.9
# Description：
"""
import os


class DevConfig:
    openaiConfig = {
        "nodes": [{"url": "https://api.openai.com", "weight": 1}],
        "timeout": 30.0,
        "keep_alive_timeout": 60.0,
        "max_connections": 10,
        "max_keep_alive_connections": 5,
        "token": "sk-xxxxxxxxxxxxxxxxxxxxx",
        "ping_path": None,
        "proxy": "http://127.0.0.1:10887"
    }


mapping = {'dev': DevConfig}
APP_ENV = os.environ.get('APP_ENV', 'dev').lower()
configuration = mapping[APP_ENV]
