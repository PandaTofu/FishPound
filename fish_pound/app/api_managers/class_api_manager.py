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
from fish_pound.db_access.database import ClassRoom
from fish_pound.db_access.constants import AccountType
from fish_pound.app.constants import *
from fish_pound.app.api_managers.base_api_manager import BaseApiManager


class ClassApiManager(BaseApiManager):
    def __init__(self, app=None, bp_name='class', url_prefix=URL_CLASS_PREFIX):
        BaseApiManager.__init__(self, app, bp_name, url_prefix)

    def init_routers(self):
        self.add_route('/page', ['GET'], 'get_class_rooms')
        self.add_route('/add', ['POST'], 'add_class_room')
        self.add_route('/join', ['POST'], 'join_class_room')

    @staticmethod
    def get_invitation_code(head_teach_id, class_room_name, enroll_year):
        name = '#'.join([str(head_teach_id), class_room_name, str(enroll_year)])
        namespace = uuid.uuid3(uuid.NAMESPACE_URL, name)
        new_uuid = uuid.uuid3(namespace, name)
        return new_uuid.hex.upper()

    @login_required
    @roles_accepted(AccountType.teacher.name)
    def get_class_rooms(self):
        page_index = request.form.get('page_index', type=int, default=None)
        page_max_items = request.form.get('page_max_items', type=int, default=None)
        head_teacher_id = request.form.get('head_teacher_id', type=int, default=current_user.teacher_cert_id)

        page_start_index = page_max_items * (page_index-1)
        page_end_index = page_start_index + page_max_items
        class_room_list = self.app.db_api.get_class_rooms_by_head_teacher(head_teacher_id)
        class_room_page = class_room_list[page_start_index:page_end_index]

        data = {'class_room_page': class_room_page}
        return create_response(EC_OK, data)

    @login_required
    @roles_accepted(AccountType.teacher.name)
    def add_class_room(self):
        class_room_name = request.form.get('name', default=None)
        enroll_year = request.form.get('enroll_year', type=int, default=None)
        head_teacher_id = request.form.get('head_teacher_id', type=int, default=current_user.teacher_cert_id)
        invitation_code = self.get_invitation_code(head_teacher_id, class_room_name, enroll_year)

        class_room = ClassRoom(class_name=class_room_name, enroll_year=enroll_year, head_teacher_id=head_teacher_id,
                               invitation_code=invitation_code)
        self.app.db_api.insert_class_room(class_room)

        data = {'invitation_code': invitation_code}
        return create_response(EC_OK, data)

    @login_required
    @roles_accepted(AccountType.parent.name)
    def join_class_room(self):
        invitation_code = request.form.get('invitation_code', default=None)
        self.app.db_api.join_class_room(current_user.id, invitation_code)


