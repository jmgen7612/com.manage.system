#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#@file   :app_start.py
#@time   :2020/4/21 18:42
#@Author :jmgen
#@Version:1.0
#@Desc   :
from app import create_app
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
from gevent import monkey
monkey.patch_all()  # 打上猴子补丁
app=create_app('default')

CORS(app,supports_credentials=True, resources={r"/auth/*": {"origins": "*"},r"/case/*": {"origins": "*"},r"/result/*": {"origins": "*"}})

#使用协程来执行程序
def app_start():
    http_server = WSGIServer(('172.22.70.204', 5000), app)
    http_server.serve_forever()
if __name__ == "__main__":
    app_start()