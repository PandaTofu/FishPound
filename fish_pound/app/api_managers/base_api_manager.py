#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Version : 1.0
# @Date    : 2019/03/31
# @Author  : PandaTofu

from collections import namedtuple
from flask import Blueprint


Router = namedtuple('Router', ['path', 'methods', 'handler'])


class BaseApiManager(object):
    def __init__(self, app=None, bp_name='base', url_prefix=None):
        self.app = None
        self.blueprint = Blueprint(bp_name, __name__, url_prefix=url_prefix)
        self.routers = list()
        self.init_app(app)

    def init_app(self, app):
        if app is None:
            return

        self.app = app
        self.init_routers()
        self.register_blueprint()

    def add_route(self, path, method, handler):
        self.routers.append(Router(path, method, handler))

    def init_routers(self):
        pass

    def register_blueprint(self):
        for router in self.routers:
            self.blueprint.route(router.path, methods=router.methods)(getattr(self, router.handler))
        self.app.register_blueprint(self.blueprint)


