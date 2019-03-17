#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Version : 1.0
# @Date    : 2019/02/20
# @Author  : PandaTofu

from flask import Blueprint, request, make_response, jsonify, current_app
from fish_pound.db_access.constants import AccountType
from fish_pound.db_access.database import User
from fish_pound.db_access.db_api import get_db_api
from fish_pound.app.constants import *
from fish_pound.app.api.user_manager import get_user_manager

account_manager = Blueprint('account', __name__, url_prefix=URL_ACCOUNT_PREFIX)


@account_manager.route(PATH_SCHOOL_LIST, methods=['GET'])
def get_school_list():
    return "No implementation."


@account_manager.route('/sign_up', methods=['POST'])
def sign_up():
    def get_response(result, error_code, http_code=HTTP_OK):
        res_body = {'result': result, 'error_code': error_code}
        return make_response(jsonify(res_body, http_code))

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

    return get_response(True, EC_OK, HTTP_OK)


@account_manager.route('/sign_in', methods=['POST'])
def sign_in():
    def get_response(result, error_code,
                     account_type=AccountType.unknown.name,
                     access_token=0,
                     http_code=HTTP_OK):
        res_body = {'result': result,
                    'error_code': error_code,
                    'type': account_type,
                    'access_token': access_token}
        return make_response(jsonify(res_body, http_code))

    phone_no = request.form.get('phone_number', None)
    password = request.form.get('password', None)

    user_manager = get_user_manager()
    user = user_manager.authenticate_by_password(phone_no, password)
    if user is None:
        return get_response(False, EC_INVALID_CREDENTIAL)
    else:
        secret_key = current_app.config.get("SECRET_KEY")
        token_life_time = current_app.config.get("TOKEN_LIFETIME")
        token = user_manager.set_token(phone_no, password, secret_key, token_life_time)
        return get_response(True, EC_OK, user.get('account_type'), token)
