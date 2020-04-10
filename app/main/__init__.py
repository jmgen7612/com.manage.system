#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#@file   :errors.py
#@time   :2020/3/2017:01
#@Author :jmgen
#@Version:1.0
#@Desc   :
from flask import Blueprint

main = Blueprint("main", __name__)

from . import views, errors