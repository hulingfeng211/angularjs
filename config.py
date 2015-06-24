#!/usr/bin/env python
# -*- coding:utf-8 -*- 
"""========================================================== 
+FileName:config.py
+Author: george
+mail:hulingfeng211@163.com
+Created Time:2015年03月27日 星期五 09时06分28秒
+Description: 项目的配置文件，所有变量都要大写
+============================================================"""
# auth uri : mongodb://user:pass@localhost:27017/database_name
import os

MONGODB_URI = 'mongodb://localhost:27017/test_database'
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'templates')
STATIC_PATH = os.path.join(os.path.dirname(__file__), 'static')
LOGIN_URL = '/login'
SITE_TITLE = '我的工作台'
#设置网络代理
#PROXY_HOST=None
#PROXY_PORT=None
UPLOAD_PATH='/data/upload/'
PROXY_HOST='192.168.2.7'
PROXY_PORT=3128
DEBUG = True
REDIS_SETTING={
    "host":"127.0.0.1",
    "port":6379,
    "db":1
}



