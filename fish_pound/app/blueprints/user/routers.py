# -*- coding: utf-8 -*-

from flask import redirect, render_template, flash, url_for, request
from flask_login import current_user, login_user
from flask_babel import _
from werkzeug.urls import url_parse
from app.blueprints.user import bp
from app.blueprints.user.forms import SignupForm, SigninForm
from database.models import User
from extensions import db


@bp.route('/signup', methods=['POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    
    form = SignupForm()
    if not form.validate_on_submit():
        return render_template(
            'user/signup.html', title=_('Register'), form=form)
    
    user = User(username=form.username.data, email=form.email.data)
    user.set_password(form.password.data)
    db.session.add(user)
    flash(_('Congratulations, you are now a registered user!'))
    return redirect(url_for('user_bp.signin'))


@bp.route('/signin', methods=['POST'])
def sign_in():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    
    form = SigninForm()
    if not form.validate_on_submit():
        return render_template('user/signin.html', title=_('Sign In'), form=form)

    user = User.query.filter_by(username=form.username.data).first()
    if user is None:
        print("User is not found.")
        flash(_('Invalid username or password'))
        return redirect(url_for('user_bp.signin'))

    if not user.verify_password(form.password.data):
        print("Incorrect Password.")
        flash(_('Invalid username or password'))
        return redirect(url_for('user_bp.signin'))
    
    login_user(user, remember=form.remember_me.data)
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('index.index')
    return redirect(next_page)
    