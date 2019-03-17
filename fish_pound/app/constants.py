#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Version : 1.0
# @Date    : 2019/02/20
# @Author  : PandaTofu

VERSION = "1.0"
DOMAIN = "FishPound"
URL_PATH_PREFIX = '/' + DOMAIN + '/' + VERSION

PATH_SCHOOL_LIST = URL_PATH_PREFIX+'/school/list/'
URL_ACCOUNT_PREFIX = URL_PATH_PREFIX + '/user'

URL_CLASS_PREFIX = URL_PATH_PREFIX + '/class'
PATH_ADD_CLASS = URL_PATH_PREFIX+'/class/add/'
PATH_INVITATION_CODE = URL_PATH_PREFIX+'/class/invitation_code/'
PATH_JOIN_CLASS = URL_PATH_PREFIX+'/class/join/'
PATH_CLASS_LIST = URL_PATH_PREFIX+'/class/list/'


# error code
EC_OK = 1000
EC_INVALID_CREDENTIAL = 1101
EC_INVALID_TOKEN = 1102
EC_NO_PERMISSION = 1103

# http code
HTTP_OK = 200

