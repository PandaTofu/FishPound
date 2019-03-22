#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Version : 1.0
# @Date    : 2019/03/12
# @Author  : PandaTofu


from functools import wraps
from flask import request, make_response, jsonify, current_app
from flask_login import LoginManager
from itsdangerous import URLSafeSerializer
from werkzeug.contrib.cache import SimpleCache
from fish_pound.utils import singleton, get_browser_id
from fish_pound.db_access.db_api import get_db_api
from fish_pound.app.constants import HTTP_OK, EC_INVALID_CREDENTIAL, EC_NO_PERMISSION


@singleton
class UserManager:
    def __init__(self, app=None):
        self.token_cache = SimpleCache()
        self.login_manager = LoginManager()
        self.db_api = get_db_api()

    def set_token(self, phone_no, password, secret_key, life_time):
        serializer = URLSafeSerializer(secret_key)
        browser_id = get_browser_id()
        token = serializer.dumps((phone_no, password, browser_id))
        self.token_cache.set(token, 1, life_time)
        return token

    def load_token(self, token):
        secret_key = current_app.config['SECRET_KEY']
        serializer = URLSafeSerializer(secret_key)
        phone_no, password, _ = serializer.loads(token)
        return self.db_api.get_user_by_password(phone_no, password)

    def authenticate_by_password(self, phone_no, password):
        return self.db_api.get_user_by_password(phone_no, password)

    def authenticate_by_token(self, token):
        if token is None:
            print("Invalid token! The token is null.")
            return None

        cached_token = self.token_cache.get(token)
        if not cached_token:
            print("Invalid token! The token is not cached.")
            return None

        secret_key = current_app.config['SECRET_KEY']
        serializer = URLSafeSerializer(secret_key)
        phone_no, password, browser_id = serializer.loads(token)
        actual_browser_id = get_browser_id()
        if actual_browser_id != browser_id:
            print("Invalid token! The user environment had changed.")
            return None

        return self.db_api.get_user_by_password(phone_no, password)


def get_user_manager():
    return UserManager()


def get_unauthorized_response(error_code):
    res_body = {'result': False, 'error_code': error_code}
    return make_response(jsonify(res_body, HTTP_OK))


def login_required(allowed_scope=None):
    def decorator(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            token = request.form.get('access_token', None)
            user_manager = get_user_manager()
            user = user_manager.authenticate_by_token(token)
            if user is None:
                return get_unauthorized_response(EC_INVALID_CREDENTIAL)

            if allowed_scope:
                account_type = user.get('account_type')
                if account_type not in allowed_scope:
                    return get_unauthorized_response(EC_NO_PERMISSION)

            return func(*args, **kwargs)

        return decorated_view

    return decorator

