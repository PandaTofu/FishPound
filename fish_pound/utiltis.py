#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Version : 1.0
# @Date    : 2019/02/24
# @Author  : PandaTofu

import hashlib
from flask import Flask, g
from fish_pound.db_access.db_api import DbApi


def generate_hash(content):
    m = hashlib.md5()
    m.update(content.encode("utf8"))
    return m.hexdigest()
