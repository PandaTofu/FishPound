#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Version : 1.0
# @Date    : 2019/02/20
# @Author  : PandaTofu

import time
from flask import Blueprint, request, make_response, jsonify, current_app
from flask_security.core import Security
from fish_pound.db_access.database import User
from fish_pound.app.constants import *
from fish_pound.utils import get_client_id, create_response


class UserApiManager(object):
    def __init__(self, app=None):
        self.app = None
        self.security_service = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.security_service = Security(app)
        self.configure_login_manager()
        self.register_blueprint()

    def configure_login_manager(self):
        login_manager = self.security_service.login_manager
        login_manager.user_loader(self._load_auth_token)
        login_manager.request_loader(self._request_loader)

    def register_blueprint(self):
        bp = Blueprint('user', __name__, url_prefix=URL_USER_PREFIX)

        bp.route('/sign_up', methods=['POST'])(self._sign_up)
        bp.route('/sign_in', methods=['POST'])(self._sign_in)

        self.app.register_blueprint(bp)
        return bp

    def _get_auth_token(self, user):
        current_time = time.time()
        serializer = self.security_service.remember_token_serializer
        return serializer.dumps((user.phone_no, user.password, current_time))

    def _load_auth_token(self, token):
        serializer = self.security_service.remember_token_serializer
        phone_no, password, _ = serializer.loads(token)

        user = self.app.db_api.get_user_by_phone_no(phone_no)
        if user and user.verify_password(password):
            return user

        return None

    def _request_loader(self, request):
        token = request.form.get('access_token', None)
        if token is None:
            print("Invalid token! The token is null.")
            return None

        client_id = self.app.token_cache.get(token)
        if not client_id:
            print("Invalid token! The token is not cached.")
            return None

        request_client_id = get_client_id(request)
        if request_client_id != client_id:
            print("Invalid token! The client had changed.")
            self.app.token_cache.delete(token)
            return None

        user = self._load_auth_token(token)
        if user is None:
            print("Invalid token! Incorrect credential.")
            self.app.token_cache.delete(token)
            return None

        return user

    def _sign_up(self):
        phone_no = request.form.get('phone_number', None)
        password = request.form.get('password', None)
        account_type = request.form.get('account_type', None)
        user_name = request.form.get('user_name', None)
        school_id = request.form.get('school_id', None)
        teacher_id = request.form.get('teacher_id', None)

        user = User(phone_no=phone_no, password=password, account_type=account_type,
                    user_name=user_name, school_id=school_id, teacher_id=teacher_id)
        self.app.db_api.insert_user(user)

        return create_response(EC_OK)

    def _sign_in(self):
        phone_no = request.form.get('phone_number', None)
        password = request.form.get('password', None)

        user = self.app.db_api.get_user_by_phone_no(phone_no)
        if user is None:
            print("User is not found.")
            return create_response(EC_INVALID_CREDENTIAL)

        if not user.verify_password(password):
            print("Password is incorrect")
            return create_response(EC_INVALID_CREDENTIAL)

        auth_token = self._get_auth_token(user)
        token_life_time = current_app.config.get("SECRET_TOKEN_LIFETIME")
        client_id = get_client_id(request)
        self.app.token_cache.set(auth_token, client_id, token_life_time)

        data = {'account_type': user.account_type.name, 'access_token': auth_token}
        return create_response(EC_OK, data)



