#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Version : 1.0
# @Date    : 2018/11/04
# @Author  : PandaTofu

DB_URL = 'mysql+pymysql://%(user)s:%(passwd)s@%(url)s/%(dbname)s' \
                    % {'user': 'root', 'passwd': '12345678', 'url': 'localhost', 'dbname': 'test'}

TYPE_TEACHER = 'Teacher'
TYPE_PARENT = 'Parent'


