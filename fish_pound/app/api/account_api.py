#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Version : 1.0
# @Date    : 2019/02/20
# @Author  : PandaTofu

from flask import Blueprint, request, make_response, jsonify
from fish_pound.utiltis import generate_hash
from fish_pound.db_access.database import User
from fish_pound.db_access.db_api import get_db_api
from fish_pound.app.constants import *

account_manager = Blueprint('account', __name__, url_prefix=URL_ACCOUNT_PREFIX)


def authenticate(user_password, input_password):
    encrypted_password = generate_hash(input_password)
    result = (encrypted_password == user_password)
    return result


@account_manager.route(PATH_SCHOOL_LIST, methods=['GET'])
def get_school_list():
    return "No implementation."


@account_manager.route('/sign_up/', methods=['POST'])
def sign_up():
    phone_no = request.form.get('phone_number', None)
    password = request.form.get('password', None)
    account_type = request.form.get('account_type', None)
    user_name = request.form.get('user_name', None)
    school_id = request.form.get('school_id', None)
    teacher_id = request.form.get('teacher_id', None)
    user = User(phone_no=phone_no, password=password, account_type=account_type,
                user_name=user_name, school_id=school_id, teacher_id=teacher_id)

    db_api = get_db_api()
    db_api.insert_user(user)

    response = jsonify({"result": True, "error_code": EC_OK}, 200)
    return make_response(response)


@account_manager.route('/sign_in/', methods=['POST'])
def sign_in():
    phone_no = request.form.get('phone_number', None)
    password = request.form.get('password', None)

    db_api = get_db_api()
    user = db_api.get_user(phone_no)

    result = authenticate(user.get('password'), password)
    error_code = EC_OK
    account_type = user.get('account_type', 'unknown')
    access_token = 0
    http_code = 200
    res_body = {'result': result,
                'error_code': error_code,
                'type': account_type,
                'access_token': access_token}

    return make_response(jsonify(res_body, http_code))
