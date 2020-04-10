#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#@file   :__init__.py
#@time   :2020/3/3011:24
#@Author :jmgen
#@Version:1.0
#@Desc   :
from flask import Blueprint

case=Blueprint("case",__name__)

from . import views