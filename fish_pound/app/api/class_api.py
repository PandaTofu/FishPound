#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Version : 1.0
# @Date    : 2019/02/20
# @Author  : PandaTofu

from flask import Blueprint
from fish_pound.app.constants import *

class_manager = Blueprint('class', __name__)


@class_manager.route(PATH_CLASS_LIST, methods=['GET'])
def get_class_list():
    pass


@class_manager.route(PATH_ADD_CLASS, methods=['POST'])
def add_class():
    pass


@class_manager.route(PATH_INVITATION_CODE, methods=['POST'])
def generate_invitation_code():
    pass


@class_manager.route(PATH_JOIN_CLASS, methods=['POST'])
def join_class():
    pass