#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Version : 1.0
# @Date    : 2019/02/20
# @Author  : PandaTofu

from flask import Blueprint, request, make_response, jsonify, current_app
from flask_login import LoginManager
from itsdangerous import URLSafeSerializer
from fish_pound.db_access.constants import AccountType
from fish_pound.db_access.database import User
from fish_pound.app.constants import *
from fish_pound.app.api.user_manager import get_user_manager
from fish_pound.utils import get_client_id

login_manager = LoginManager()
account_api_manager = Blueprint('account', __name__, url_prefix=URL_ACCOUNT_PREFIX)


def create_token(request, phone_no, password, secret_key):
    serializer = URLSafeSerializer(secret_key)
    client_id = get_client_id(request)
    token = serializer.dumps((phone_no, password, client_id))
    return token


@login_manager.request_loader
def load_user_from_token(request):
    token = request.form.get('access_token', None)
    if token is None:
        print("Invalid token! The token is null.")
        return None

    cached_token = current_app.token_cache.get(token)
    if not cached_token:
        print("Invalid token! The token is not cached.")
        return None

    secret_key = current_app.config['SECRET_KEY']
    serializer = URLSafeSerializer(secret_key)
    phone_no, password, client_id = serializer.loads(token)

    client_id_in_request = get_client_id(request)
    if client_id_in_request != client_id:
        print("Invalid token! The client had changed.")
        return None

    return current_app.db_api.get_user_by_password(phone_no, password)


@account_api_manager.route('/sign_up', methods=['POST'])
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

    current_app.db_api.insert_user(user)

    return get_response(True, EC_OK, HTTP_OK)


@account_api_manager.route('/sign_in', methods=['POST'])
def sign_in():
    def get_response(result, error_code,
                     account_type_name=AccountType.unknown.name,
                     access_token=0,
                     http_code=HTTP_OK):
        res_body = {'result': result,
                    'error_code': error_code,
                    'type': account_type_name,
                    'access_token': access_token}
        return make_response(jsonify(res_body, http_code))

    phone_no = request.form.get('phone_number', None)
    password = request.form.get('password', None)

    user = current_app.db_api.get_user_by_password(phone_no, password)
    if user is None:
        return get_response(False, EC_INVALID_CREDENTIAL)
    else:
        secret_key = current_app.config.get("SECRET_KEY")
        token_life_time = current_app.config.get("TOKEN_LIFETIME")
        token = create_token(request, phone_no, password, secret_key)
        current_app.token_cache.set(token, 1, token_life_time)
        account_type = user.get('account_type').name
        return get_response(True, EC_OK, account_type, token)
