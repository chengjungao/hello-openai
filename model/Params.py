# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : Params.py
# Time       ：2023/3/25 00:01
# Author     ：Cheng Jungao
# version    ：python 3.9
# Description：
"""

from pydantic import BaseModel


class Params(BaseModel):
    prompt: str
