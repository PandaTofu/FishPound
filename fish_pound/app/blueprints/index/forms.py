# -*- coding: utf-8 -*-


from flask_wtf import FlaskForm
from flask_babel import _, lazy_gettext as lzgt
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from database.models import User


class SignupForm(FlaskForm):
    username = StringField(lzgt('Username'), validators=[DataRequired()])
    email = StringField(lzgt('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(lzgt('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        lzgt('Repeat Password'), 
        validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField(lzgt('Sign up'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different username.'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different email address.'))


class SigninForm(FlaskForm):
    username = StringField(lzgt('Username'), validators=[DataRequired()])
    password = PasswordField(lzgt('Password'), validators=[DataRequired()])
    remember_me = BooleanField(lzgt('Remember Me'))
    submit = SubmitField(lzgt('Sign In'))

