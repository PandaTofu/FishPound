# -*- coding: utf-8 -*-

from flask import redirect, render_template, flash, url_for, request
from flask_login import current_user, login_user
from flask_babel import _
from werkzeug.urls import url_parse
from app.blueprints.index import bp
from database.models import User
from extensions import db


@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
def index():
    return render_template('index.html', title=_('Home'), form=None)
    