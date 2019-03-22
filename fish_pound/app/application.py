#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Version : 1.0
# @Date    : 2019/02/20
# @Author  : PandaTofu

from flask import Flask
from flask_login import LoginManager
from werkzeug.contrib.cache import SimpleCache
from fish_pound.db_access.db_api import DbApi
from fish_pound.app.config import config
from fish_pound.app.api.account_api import account_api_manager, login_manager


app_cache = SimpleCache()


def setup_app(app, app_config):
    # load app configuration
    app.config.from_object(app_config)

    # init db api
    db_api = DbApi()
    db_api.init_app(app)

    # init token cache
    token_cache = SimpleCache()
    app.token_cache = token_cache

    # init login manager
    login_manager.init_app(app)

    # register blueprint
    app.register_blueprint(account_api_manager)


def create_app(config_key_name):
    app = Flask(__name__)

    app_config = config[config_key_name]
    setup_app(app, app_config)

    return app


