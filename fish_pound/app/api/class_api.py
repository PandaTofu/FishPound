#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Version : 1.0
# @Date    : 2019/02/20
# @Author  : PandaTofu

from flask import Blueprint, request, make_response, jsonify
from fish_pound.db_access.database import Class
from fish_pound.db_access.constants import AccountType
from fish_pound.app.api.user_manager import get_user_manager, login_required
from fish_pound.app.constants import *

class_api_manager = Blueprint('class', __name__, url_prefix=URL_CLASS_PREFIX)


@class_api_manager.route('/list', methods=['GET'])
@login_required(allowed_scope=[AccountType.teacher.name])
def get_class_list():
    def get_response(result, error_code, filtered_class_list, http_code=HTTP_OK):
        res_body = {'result': result, 'error_code': error_code, 'class_list': filtered_class_list}
        return make_response(jsonify(res_body, http_code))

    token = request.form.get('access_token', None)
    max_item_number = request.form.get('max_item_number', None)

    user_manager = get_user_manager()
    user = user_manager.load_token(token)

    db_api = get_db_api()
    teacher_id = user.get('teacher_id')
    class_list = db_api.get_classes_by_teacher_id(teacher_id)
    class_list_page = class_list[0:max_item_number] if max_item_number < len(class_list) else class_list

    return get_response(True, EC_OK, class_list_page)


@class_api_manager.route('/add', methods=['POST'])
def add_class():

    pass


@class_manager.route(PATH_INVITATION_CODE, methods=['POST'])
def generate_invitation_code():
    pass


@class_manager.route(PATH_JOIN_CLASS, methods=['POST'])
def join_class():
    pass