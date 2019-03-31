#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Version : 1.0
# @Date    : 2019/02/24
# @Author  : PandaTofu

import hashlib
import json
from flask import make_response, jsonify


def singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton


def generate_hash(content):
    m = hashlib.md5()
    m.update(content.encode("utf8"))
    return m.hexdigest()


def get_remote_addr(request):
    """get remote client address"""
    address = request.headers.get('X-Forwarded-For', request.remote_addr)
    if not address:
        address = address.encode('utf-8').split(b',')[0].strip()
    return address


def get_client_id(request):
    """
    :param request: [flask request] request received from client
    :return: [string] client browser id
    """
    agent = request.headers.get('User-Agent')
    if not agent:
        agent = str(agent).encode('utf-8')
    base_str = "%s|%s" % (get_remote_addr(request), agent)
    return generate_hash(base_str)


def create_response(return_code=None, data=None, status_code=200):
    """
    :param return_code: the error code return by app server
    :param data: response data, different api_managers return different data
    :param status_code: http status code
    :return: http response
    """
    res_body = dict()
    if return_code:
        res_body['return_code'] = return_code
    if data:
        res_body['data'] = data

    return make_response(jsonify(res_body), status_code)



