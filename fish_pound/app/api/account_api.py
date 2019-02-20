__author__ = 'lyliu'

from flask import Blueprint
from fish_pound.app.constants import *

account_manager = Blueprint('account', __name__)


@account_manager.route(PATH_SCHOOL_LIST, methods=['GET'])
def get_school_list():
    pass



@account_manager.route(PATH_SIGN_UP, methods=['POST'])
def sign_up():
    pass


@account_manager.route(PATH_SIGN_IN, methods=['POST'])
def sign_in():
    pass