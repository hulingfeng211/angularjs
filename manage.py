#!/usr/bin/env python
# -*- coding:utf-8 -*- 
"""========================================================== 
+FileName:manage.py
+Author: george
+mail:hulingfeng211@163.com
+Created Time:2015年03月27日 星期五 08时55分23秒
+Description:
+============================================================"""
from tornado.httpclient import AsyncHTTPClient
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, parse_command_line, options
from tornado.web import Application

import config
from core import load_settings, StaticHandler
from handlers.demo import HTTPDemoHandler, UserHandler


define('port', default=8888, help='run HTTP server on this port', type=int)
define('cmd', default='runserver', help='command for task.runserver', type=str)


class MyApplication(Application):
    """"""

    def __init__(self):
        settings = load_settings(config)
        handlers = [
            (r'/$', StaticHandler, dict(
                template_name='index.html',
                title=settings['site_title']
            )),
            (r'/drag', StaticHandler, dict(
                template_name='draggable.html',
                title=settings['site_title']
            )),
            (r'/http', StaticHandler, dict(
                template_name='httpdemo.html',
                title=settings['site_title']
            )),
            (r'/demo', HTTPDemoHandler),
            (r'/demo/quickstart',StaticHandler,dict(
                template_name='quickstart.html'
            )),
            (r'/user/list', UserHandler),
            (r'/user', UserHandler),#post
            (r'/user/(\w+)', UserHandler),#delete
        ]

        self.db = settings['db']
        self.dbsync = settings['dbsync']

        Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    parse_command_line()
    AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")
    if options.cmd == 'runserver':
        app = MyApplication()
        http_server = HTTPServer(app)
        http_server.listen(options.port)
        IOLoop.instance().start()


