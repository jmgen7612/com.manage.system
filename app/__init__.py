#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#@file   :errors.py
#@time   :2020/3/2017:01
#@Author :jmgen
#@Version:1.0
#@Desc   :
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_migrate import Migrate
from config import config

db=SQLAlchemy()
bootstrap=Bootstrap()
moment=Moment()
migrate=Migrate()

def create_app(config_name):
    app=Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    moment.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .case import case as case_blueprint
    app.register_blueprint(case_blueprint, url_prefix='/case')

    from .result import result as result_blueprint
    app.register_blueprint(result_blueprint, url_prefix='/result')
    # with app.app_context():
    #     db.create_all()
    return app