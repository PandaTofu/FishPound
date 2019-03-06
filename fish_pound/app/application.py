#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Version : 1.0
# @Date    : 2019/02/20
# @Author  : PandaTofu

from flask import Flask, g
from fish_pound.app.config import config
from fish_pound.app import utiltis
from fish_pound.app.api.account_api import account_manager


def init_app(app, config_key_name):
    app.config.from_object(config[config_key_name])
    utiltis.set_db_api(app.config["DB_URL"])
    app.register_blueprint(account_manager)


def create_app(config_key_name):
    app = Flask(__name__)
    init_app(app, config_key_name)
    return app


