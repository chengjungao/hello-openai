# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : DemoRest.py
# Time       ：2023/3/23 23:15
# Author     ：Cheng Jungao
# version    ：python 3.9
# Description：
"""
from fastapi import APIRouter

from model.Params import Params
from service.OpenaiRestService import OpenaiRestService

router = APIRouter()

openai = OpenaiRestService()


@router.post("/completions")
def completions(params: Params) -> dict:
    return openai.completions(params)
