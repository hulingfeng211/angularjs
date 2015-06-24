# -*- coding:utf-8 -*-
from bson.objectid import ObjectId

__author__ = 'george'
import tornado
import tornado.web
import tornado.escape
import core


class HTTPDemoHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        names = []
        for i in xrange(100):
            names.append('Name%s' % i)
        self.write(tornado.escape.json_encode(names))


class UserHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        db = self.application.dbsync
        users = list(db.angular.find())
        """get user list """
        self.write(core.json_encode(users))

    def post(self, *args, **kwargs):
        """保存数据到mongodb"""
        db = self.application.dbsync
        user = tornado.escape.json_decode(self.request.body)
        if user.get('_id', None):
            db.angular.update({'_id': ObjectId(user['_id'])},
                              {key: value for key, value in user.items() if key != "_id"})
            pass
        else:
            db.angular.insert({key: value for key, value in user.items() if key != "_id"})
        self.write(dict(
            success=True,
            msg="保存成功"
        ))

    def delete(self, *args, **kwargs):
        """删除指定的用户"""
        if len(args) > 0:
            db = self.application.dbsync
            db.angular.remove({"_id": ObjectId(args[0])})

        self.write(dict(
            success=True,
            msg="删除成功"
        ))



