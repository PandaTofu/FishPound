#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Version : 1.0
# @Date    : 2019/02/20
# @Author  : PandaTofu

import time
from flask import Blueprint, request, make_response, jsonify, Response, abort
from flask_security.core import Security
from fish_pound.utils import get_client_id, create_response
from fish_pound.db_access.database import User
from fish_pound.app.constants import *
from fish_pound.app.api_managers.base_api_manager import BaseApiManager


class UserApiManager(BaseApiManager):
    def __init__(self, app=None, bp_name='user', url_prefix=URL_USER_PREFIX):
        self.security_service = None
        self.login_unauthorized_callback = None
        self.token_unauthorized_callback = None
        self.user_loader_callback = None
        self.request_loader_callback = None
        BaseApiManager.__init__(self, app, bp_name, url_prefix)

    def init_app(self, app):
        if app is None:
            return

        self.app = app
        self.init_routers()
        self.register_blueprint()
        self.init_security_service()

    def init_routers(self):
        self.add_route('/sign_up', ['POST'], '_sign_up')
        self.add_route('/sign_in', ['POST'], '_sign_in')

    def init_security_service(self):
        self.security_service = Security()
        self.security_service._state = self.security_service.init_app(self.app)
        self.user_loader(self._load_auth_token)
        self.request_loader(self._request_loader)
        self.login_unauthorized_handler(self._login_unauthorized_handler)
        self.token_unauthorized_handler(self._token_unauthorized_handler)

    def _get_auth_token(self, phone_no, password):
        current_time = time.time()
        serializer = self.security_service.remember_token_serializer
        return serializer.dumps((phone_no, password, current_time))

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
        nick_name = request.form.get('nick_name', None)
        school_id = request.form.get('school_id', None)
        teacher_cert_id = request.form.get('teacher_cert_id', None)

        user = User(phone_no=phone_no, password=password, account_type=account_type,
                    nick_name=nick_name, school_id=school_id, teacher_cert_id=teacher_cert_id)
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

        auth_token = self._get_auth_token(phone_no, password)
        token_life_time = self.app.config.get("SECRET_TOKEN_LIFETIME")
        client_id = get_client_id(request)
        self.app.token_cache.set(auth_token, client_id, token_life_time)

        data = {'account_type': user.account_type.name, 'access_token': auth_token}
        return create_response(EC_OK, data)

    @staticmethod
    def _login_unauthorized_handler():
        abort(Response(response='Unauthorized.', status=401))

    @staticmethod
    def _token_unauthorized_handler():
        abort(Response(response='Permission Deny.', status=401))

    def user_loader(self, callback):
        self.user_loader_callback = callback
        self.security_service.login_manager.user_loader(self.user_loader_callback)
        return callback

    def request_loader(self, callback):
        self.request_loader_callback = callback
        self.security_service.login_manager.request_loader(self.request_loader_callback)
        return callback

    def login_unauthorized_handler(self, callback):
        self.login_unauthorized_callback = callback
        self.security_service.login_manager.unauthorized_handler(self.login_unauthorized_callback)
        return callback

    def token_unauthorized_handler(self, callback):
        self.token_unauthorized_callback = callback
        self.security_service.unauthorized_handler(self.token_unauthorized_callback)
        return callback

