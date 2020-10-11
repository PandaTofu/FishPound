#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Version : 1.0
# @Date    : 2019/02/24
# @Author  : PandaTofu

import os
import platform


basedir = os.path.abspath(os.path.dirname(__file__))
#load_dotenv(os.path.join(basedir, '.env'))

class Config:
    """base config"""
    HOST = "127.0.0.1"
    PORT = 444
    DEBUG = True
    SECRET_KEY = 'dnuoPhsiF'
    SECRET_REMEMBER_SALT = 'toBeOrNotToBe'
    SECRET_TOKEN_LIFETIME = 3600


class ProConfig(Config):
    """running evn config"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://%(user)s:%(passwd)s@%(url)s/%(dbname)s' \
            % {'user': 'root', 'passwd': 'FishPound2019!', 
               'url': 'localhost', 'dbname': 'test_product'}


class TestConfig(Config):
    """testing config"""
    db_urls = {
        'Linux': 'mysql+pymysql://%(user)s:%(passwd)s@%(url)s/%(dbname)s' \
            % {'user': 'root', 'passwd': 'FishPound2019!', 
               'url': 'localhost', 'dbname': 'test'},
        'Darwin': 'sqlite:///' + os.path.join(basedir, 'test.db')
               
    }
    
    SQLALCHEMY_DATABASE_URI = db_urls[platform.system()]


config = {
    'testing': TestConfig,
    'product': ProConfig
}
