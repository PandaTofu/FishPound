#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Version : 1.0
# @Date    : 2018/11/04
# @Author  : PandaTofu

import pytest
from sqlalchemy import create_engine

from fish_pound.db_access.database import *
from fish_pound.db_access.db_api import *
from fish_pound.db_access.constants import DB_URL, TYPE_TEACHER, TYPE_PARENT


TEST_DB_URL = 'mysql+pymysql://%(user)s:%(passwd)s@%(url)s/%(dbname)s' \
                    % {'user': 'root', 'passwd': '12345678', 'url': 'localhost', 'dbname': 'test'}
TEST_PHONE_NO = "12341231234"


def init_db():
    engine = create_engine(TEST_DB_URL, encoding='utf-8', echo=True)
    BaseModel.metadata.create_all(engine)


def drop_db():
    engine = create_engine(TEST_DB_URL, encoding='utf-8', echo=True)
    BaseModel.metadata.drop_all(engine)


def setup_module(module):
    print('-------init db---------')
    init_db()


def teardown_module(module):
    print('-------drop db---------')
    drop_db()


def test_user():
    db_api = DbApi(TEST_DB_URL)
    db_api.insert_user(User(phone_no=TEST_PHONE_NO, password="fish_pound_1", account_type=TYPE_PARENT))
    user = db_api.get_user(phone_no=TEST_PHONE_NO)
    assert user.get('password') == encrypt_password("fish_pound_1")

    db_api.update_user(phone_no=TEST_PHONE_NO, password="fish_pound_2")
    user = db_api.get_user(phone_no=TEST_PHONE_NO)
    assert user.get('password') == encrypt_password("fish_pound_2")

    db_api.delete_user(phone_no=TEST_PHONE_NO)
    user = db_api.get_user(phone_no=TEST_PHONE_NO)
    assert user is None
