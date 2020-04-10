#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#@file   :views.py
#@time   :2020/3/2021:05
#@Author :jmgen
#@Version:1.0
#@Desc   :
import hashlib
from flask import request,jsonify
from . import auth
from .. import db
from ..models import User
from .forms import RegistrationForm

@auth.route("/login",methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if username and password:
        user = User.query.filter_by(username=username).first()
        if user is None:
            user = User.query.filter_by(email=username).first()
        if user is not None and user.verify_password(password):
            token = hashlib.md5(username.encode("utf-8")).hexdigest()
            gravatar=user.gravatar()
            return jsonify({'code': 200, 'msg': 'ok', 'token': token, 'username': username, 'gravatar': gravatar})
        else:
            return jsonify({'code': 20001, 'msg': '账号或密码错误，请输入正确的账号密码'})

@auth.route("/register", methods=['POST'])
def register():
    form = RegistrationForm()
    email = request.json.get('email')
    username = request.json.get('username')
    password = request.json.get('password')
    if form.validate_email(email) and form.validate_username(username):
        if email and username and password:
            avatar_hash = hashlib.md5(email.encode("utf-8")).hexdigest()
            user = User(email=email, username=username, password=password,
                        avatar_hash=avatar_hash)
            db.session.add(user)
            db.session.commit()
            return jsonify({'code': 200})
    else:
        return jsonify({'code': 20005 , 'msg': '用户名或邮箱已存在，请重新输入'})