# -*- coding:utf-8 -*-
from json import JSONEncoder
import json
import sys
import os
from bson import ObjectId
import motor
from pymongo import MongoClient
from tornado.web import authenticated, RequestHandler, HTTPError
import tornadoredis
from torndsession.sessionhandler import SessionBaseHandler
from core.utils import load_config, make_cookie_securety
__author__ = 'george'


class BaseHandler(SessionBaseHandler):
    def initialize(self, **kwargs):
        if kwargs:
            for key, val in kwargs.items():
                if not hasattr(self, key):
                    setattr(self, key, val)
        if not hasattr(self, 'db'):
            setattr(self, 'db', self.application.db)
        if not hasattr(self, 'dbsync'):
            setattr(self, 'dbsync', self.application.dbsync)

        super(BaseHandler, self).initialize()

    def get_current_user(self):
        session_id = self.session.id
        if session_id:
            return self.session.get('user', None)

        return None

    @authenticated
    def prepare(self):
        # update expires
        self.session.set('expires', 1200)

        pass

class NOAuthStaticHandler(BaseHandler):
    """
    负责处理所有静态文件的请求，属于完全开放的页面，不需要身份认证
    """
    def prepare(self):
        pass

    def get(self, *args, **kwargs):
        self.render(self.template_name, title=self.title )

class StaticHandler(RequestHandler):
    """
    负责处理所有静态文件的请求，需要登陆的用户才能进行访问，未授权则自动跳转到登陆页面进行身份认证
    """
    def initialize(self, **kwargs):
        if kwargs:
            for key, val in kwargs.items():
                if not hasattr(self, key):
                    setattr(self, key, val)
        if not hasattr(self, 'db'):
            setattr(self, 'db', self.application.db)
        if not hasattr(self, 'dbsync'):
            setattr(self, 'dbsync', self.application.dbsync)

        super(StaticHandler, self).initialize()

    def get(self, *args, **kwargs):
        #self.render(self.template_name, title=self.title, user=self.current_user)
        template_path = self.get_template_path()
        if  template_path:
            template_path = os.path.join(template_path,self.template_name)
            #todo read file content write to browser
            with open(template_path) as file:
                map(self.write,(line for line in file.readlines()))
        else:
            raise HTTPError(status_code=404,log_message="模版没有找到")



class MongoEncoder(JSONEncoder):
    def default(self, obj, **kwargs):
        if isinstance(obj, ObjectId):
            return str(obj)
        else:
            return JSONEncoder.default(obj, **kwargs)


def json_encode(obj):
    """特殊处理MONGODB的OBJECTID"""
    return json.dumps(obj, cls=MongoEncoder)


def load_settings(config):
    settings = load_config(config)
    db = motor.MotorClient(config.MONGODB_URI)['test_database']  # 异步方式的DB对象
    dbsync = MongoClient(config.MONGODB_URI)['test_database']  # 同步方式的DB对象
    redis = tornadoredis.Client(host=config.REDIS_SETTING['host'],
                                port=config.REDIS_SETTING['port'],
                                selected_db=config.REDIS_SETTING['db'])
    redis.connect()

    settings.update({'db': db})
    settings.update({'dbsync': dbsync})
    settings.update({"cookie_secret": make_cookie_securety()})
    settings.update({'redis': redis})
    return settings
