#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Version : 1.0
# @Date    : 2019/02/20
# @Author  : PandaTofu

from flask import Flask
from sqlalchemy import create_engine
from fish_pound.db_access.database import *
from fish_pound.db_access.db_api import *
from fish_pound.app.config import config
from fish_pound.app.api.account_api import account_manager


def init_db(app):
    db_url = app.config['DB_URL']
    engine = create_engine(db_url, encoding='utf-8', echo=True)
    BaseModel.metadata.create_all(engine)
    get_db_api(db_url)


def init_app(app, config_key_name):
    app.config.from_object(config[config_key_name])
    app.register_blueprint(account_manager)


def create_app(config_key_name):
    app = Flask(__name__)
    init_app(app, config_key_name)
    init_db(app)
    return app


