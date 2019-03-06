#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Version : 1.0
# @Date    : 2019/02/24
# @Author  : PandaTofu

from flask import Flask, g
from fish_pound.db_access.db_api import DbApi


def set_db_api(db_url):
    g.db_api = DbApi(db_url)


def get_db_api():
    return getattr(g, 'db_api', None)
