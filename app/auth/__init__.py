#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#@file   :__init__.py.py
#@time   :2020/3/2021:04
#@Author :jmgen
#@Version:1.0
#@Desc   :
from flask import Blueprint

auth=Blueprint("auth",__name__)

from . import views