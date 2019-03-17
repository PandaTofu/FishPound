#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Version : 1.0
# @Date    : 2019/02/24
# @Author  : PandaTofu


class Config:
    """base config"""
    HOST = "127.0.0.1"
    PORT = 443
    DEBUG = True
    SECRET_KEY = 'dnuoPhsiF'
    TOKEN_LIFETIME = 3600


class ProConfig(Config):
    """running evn config"""
    DB_URL = 'mysql+pymysql://%(user)s:%(passwd)s@%(url)s/%(dbname)s' \
         % {'user': 'root', 'passwd': 'FishPound2019!', 'url': 'localhost', 'dbname': 'test_product'}


class TestConfig(Config):
    """testing config"""
    DB_URL = 'mysql+pymysql://%(user)s:%(passwd)s@%(url)s/%(dbname)s' \
         % {'user': 'root', 'passwd': 'FishPound2019!', 'url': 'localhost', 'dbname': 'test'}


config = {
    'testing': TestConfig,
    'product': ProConfig
}
