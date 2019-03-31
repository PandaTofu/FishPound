#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Version : 1.0
# @Date    : 2019/02/20
# @Author  : PandaTofu

import uuid
from flask import Blueprint, request, make_response, jsonify, current_app, abort
from flask_login import login_required, current_user
from flask_security.decorators import login_required, roles_accepted
from fish_pound.utils import create_response
from fish_pound.db_access.database import Class
from fish_pound.db_access.constants import AccountType
from fish_pound.app.constants import *
from fish_pound.app.api_managers.base_api_manager import BaseApiManager


class ClassApiManager(BaseApiManager):
    def __init__(self, app=None, bp_name='class', url_prefix=URL_CLASS_PREFIX):
        BaseApiManager.__init__(self, app, bp_name, url_prefix)

    def init_routers(self):
        self.add_route('/list', ['GET'], 'get_class_list')
        self.add_route('/add', ['POST'], 'add_class')

    @staticmethod
    def get_invitation_code(teach_id, class_name, enroll_year):
        name = '#'.join([str(teach_id), class_name, str(enroll_year)])
        namespace = uuid.uuid3(uuid.NAMESPACE_URL, name)
        new_uuid = uuid.uuid3(namespace, name)
        return new_uuid.hex.upper()

    @login_required
    @roles_accepted(AccountType.teacher.name)
    def get_class_list(self):
        max_item_number = request.form.get('max_item_number', type=int, default=None)
        teacher_id = request.form.get('teacher_id', type=int, default=current_user.teacher_id)

        class_list = self.app.db_api.get_classes_by_teacher_id(teacher_id)
        class_list_page = class_list[0:max_item_number] if max_item_number < len(class_list) else class_list

        data = {'class_list': class_list_page}
        return create_response(EC_OK, data)

    @login_required
    @roles_accepted(AccountType.teacher.name)
    def add_class(self):
        class_name = request.form.get('class_name', default=None)
        enroll_year = request.form.get('enroll_year', type=int, default=None)
        teacher_id = request.form.get('teacher_id', type=int, default=current_user.teacher_id)
        invitation_code = self.get_invitation_code(teacher_id, class_name, enroll_year)

        class_record = Class(class_name=class_name, enroll_year=enroll_year,
                             teacher_id=teacher_id, invitation_code=invitation_code)
        class_id = self.app.db_api.insert_class(class_record)

        data = {'class_id': class_id}
        return create_response(EC_OK, data)
