#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Version : 1.0
# @Date    : 2019/02/20
# @Author  : PandaTofu

import uuid
from flask import Blueprint, request, make_response, jsonify, current_app, abort
from flask_login import login_required, current_user
from fish_pound.db_access.database import Class
from fish_pound.db_access.constants import AccountType
from fish_pound.app.constants import *
from fish_pound.utils import create_response

class_api_manager = Blueprint('class', __name__, url_prefix=URL_CLASS_PREFIX)


def generate_invitation_code(class_name, enroll_year):
    name = class_name + '#' + str(enroll_year)
    namespace = uuid.uuid3(uuid.NAMESPACE_URL, name)
    new_uuid = uuid.uuid3(namespace, name)
    return new_uuid.hex.upper()


@class_api_manager.route('/list', methods=['GET'])
@login_required
def get_class_list():
    def get_response(result, error_code, filtered_class_list, http_code=HTTP_OK):
        res_body = {'result': result, 'error_code': error_code, 'class_list': filtered_class_list}
        return make_response(jsonify(res_body, http_code))

    max_item_number = request.form.get('max_item_number', type=int, default=None)
    teacher_id = current_user.get('teacher_id')

    class_list = current_app.db_api.get_classes_by_teacher_id(teacher_id)
    class_list_page = class_list[0:max_item_number] if max_item_number < len(class_list) else class_list

    data = {'class_list': class_list_page}
    return create_response(EC_OK, data)


@class_api_manager.route('/add', methods=['POST'])
@login_required
def add_class():
    class_name = request.form.get('class_name', default=None)
    enroll_year = request.form.get('enroll_year', type=int, default=None)
    teacher_id = current_user.get('teacher_id')
    invitation_code = generate_invitation_code(class_name, enroll_year)

    class_record = Class(class_name=class_name, enroll_year=enroll_year,
                         teacher_id=teacher_id, invitation_code=invitation_code)
    class_id = current_app.db_api.insert_class(class_record)

    data = {'class_id': class_id}
    return create_response(EC_OK, data)


@class_api_manager.route(PATH_JOIN_CLASS, methods=['POST'])
def join_class():
    pass