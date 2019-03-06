#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Version : 1.0
# @Date    : 2019/02/20
# @Author  : PandaTofu

from flask import Blueprint, request, make_response, jsonify
from fish_pound.app import utiltis
from fish_pound.db_access.database import User
from fish_pound.app.constants import *

account_manager = Blueprint('account', __name__, url_prefix=URL_ACCOUNT_PREFIX)


@account_manager.route(PATH_SCHOOL_LIST, methods=['GET'])
def get_school_list():
    return "No implementation."


@account_manager.route('/sign_up/', methods=['POST'])
def sign_up():
    db_api = utiltis.get_db_api()
    if db_api is None:
        return make_response(jsonify({}, 500))

    phone_no = request.form.get('phone_number', None)
    password = request.form.get('password', None)
    account_type = request.form.get('account_type', None)
    user_name = request.form.get('user_name', None)
    school_id = request.form.get('school_id', None)
    teacher_id = request.form.get('teacher_id', None)

    user = User(phone_no=phone_no, password=password, account_type=account_type,
                user_name=user_name, school_id=school_id, teacher_id=teacher_id)
    db_api.insert_user(user)

    response = jsonify({"result": True, "error_code": EC_OK}, 200)
    return make_response(response)


@account_manager.route('/sign_in/', methods=['POST'])
def sign_in():
    return "No implementation."
