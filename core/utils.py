#!/usr/bin/env python
# -*- coding:utf-8 -*- 
"""========================================================== 
+FileName:utils.py
+Author: george
+mail:hulingfeng211@163.com
+Created Time:2015年03月27日 星期五 09时10分17秒
+Description:常用到的工具方法
+============================================================"""
import base64
from hashlib import md5
import sys
import time
import uuid

from pymongo import MongoClient
from tornado import httpclient
from tornado import escape

import config
from core import constants


def get_access_token(settings):

    redis_client = settings['redis']

    wei_setting = settings['weixin_setting']
    corpid = wei_setting['corpid']
    secret = wei_setting['secret']
    access_token_url = wei_setting['access_token_url'] % dict(
        corpid=corpid,
        secret=secret
    )

    http_client = httpclient.HTTPClient()
    response = http_client.fetch(access_token_url, proxy_host=settings['proxy_host'], proxy_port=settings['proxy_port'])
    result = escape.json_decode(response.body)
    access_token = result.get(constants.ACCESS_TOKEN)
    if result and access_token:  # get right access token
        redis_client.set(constants.ACCESS_TOKEN, access_token, result['expires_in'])
    if access_token:
        return access_token


def load_config(config):
    """从配置模块中加载项目的配置选项，返回一个字典"""
    settings = {}
    for key in dir(config):
        if key.isupper():
            settings[key.lower()] = getattr(config, key)
    return settings


def make_password(raw_password):
    return md5(raw_password).hexdigest()


def make_cookie_securety():
    return base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)


def create_user():
    cursor = MongoClient(config.MONGODB_URI)
    db = cursor['test_database']
    username = raw_input('please input amdin username:')
    if not username:
        print 'must input username'
    else:
        exist_user = db.users.find_one({'username': username})
        if exist_user:
            print 'user existed in system,other username can input.'
            sys.exit(0)

    email = raw_input('please input amdin email:')
    if not email:
        print 'must input admin email'
        sys.exit(0)
    else:
        exist_email = db.users.find_one({'email': email})
        if exist_email:
            print 'email already use by other'
            sys.exit()
    password = raw_input('please input admin  password:')
    if not password:
        print 'must input admin password'
        sys.exit(0)
    else:
        # regex=re.compile(r'/^[a-zA-Z\d_]{8,}$')
        # print regex.findall(password)
        if len(password) < 6:
            print 'password minlength great than 6'
            sys.exit(0)
    user = {
        'username': username,
        'email': email,
        'password': make_password(password),
        'registe_date': time.time(),
        'is_super_user': True
    }
    db.users.insert(user)
    cursor.close()





