# -*- coding: utf-8 -*-
#
# @Version : 1.0
# @Date    : 2020/10/11
# @Author  : PandaTofu

from flask import Flask
from config import config
from extensions import db


def create_app(config_key_name):
    app = Flask(__name__)

    # load app configuration
    app_config = config[config_key_name]
    app.config.from_object(app_config)

    # bind db to app
    db.init_app(app)

    #register blueprints
    from app.blueprints import user_bp
    app.register_blueprint(user_bp, url_prefix='/user')

    from app.blueprints import index_bp
    app.register_blueprint(index_bp)

    return app