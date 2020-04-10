#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#@file   :forms.py
#@time   :2020/3/2021:05
#@Author :jmgen
#@Version:1.0
#@Desc   :
from wtforms import StringField,PasswordField,SubmitField,Form
from wtforms.validators import DataRequired,Length,Email,EqualTo,Regexp
from ..models import User

class LoginForm(Form):
    # username = StringField(u"用户名")
    # email = StringField(u'电子邮件')
    # password = PasswordField(u'密码')
    username = StringField(u"用户名", validators=[DataRequired(message="sasas"), Length(1, 2, message="sdsd"), Email(message="太难吃")])
    email = StringField(u'电子邮件', validators=[DataRequired(), Length(1, 64),Email()])
    password = PasswordField(u'密码', validators=[DataRequired()])

class RegistrationForm(Form):
    # email = StringField(u'邮箱')
    # username = StringField(u'用户名')
    # password = PasswordField(u'密码')
    # password2 = PasswordField(u'重复密码')
    # submit = SubmitField(u'注册')
    email = StringField(u'邮箱', validators=[DataRequired(), Length(1, 64),Email()])
    username = StringField(u'用户名', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               u'用户名必须是字母、数字、点号或者下划线组成')])
    password = PasswordField(u'密码', validators=[
        DataRequired(), EqualTo('password2', message=u'密码必须一致')])
    password2 = PasswordField(u'重复密码', validators=[DataRequired()])
    submit = SubmitField(u'注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field).first():
            return False
        else:
            return True

    def validate_username(self, field):
        if User.query.filter_by(username=field).first():
            return False
        else:
            return True