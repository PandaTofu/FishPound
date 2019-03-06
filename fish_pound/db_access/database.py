#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Version : 1.0
# @Date    : 2018/11/04
# @Author  : PandaTofu

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, Boolean, Enum
from sqlalchemy.dialects.mysql import INTEGER
from db_access.constants import TYPE_TEACHER, TYPE_PARENT

BaseModel = declarative_base()


class BaseModel(BaseModel):
    __abstract__ = True

    def verify(self):
        return True

    def update(self, attrs):
        for key, value in attrs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def get(self, key):
        return getattr(self, key, None)


class User(BaseModel):
    __tablename__ = u'user'

    phone_no = Column(String(20), primary_key=True)
    password = Column(String(50), nullable=False)
    account_type = Column(Enum(TYPE_TEACHER, TYPE_PARENT), nullable=False)
    user_name = Column(String(50))
    school_id = Column(Integer)
    teacher_id = Column(Integer)
    activated = Column(Boolean, default=False)

    def verify(self):
        if self.account_type == TYPE_TEACHER and self.teacher_id is None:
            raise ValueError("No teacher_id for user[%s]" % self.phone_no)

    def is_active(self):
        return self.activated

    def is_authenticated(self):
        #"""假设已经通过验证"""
        return True

    def is_anonymous(self):
        #"""具有登录名和密码的账号不是匿名用户"""
        return False


class School(BaseModel):
    __tablename__ = 'school'

    school_id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    school_name = Column(String(50))
    address = Column(String(100))


class Class(BaseModel):
    __tablename__ = 'class'

    class_id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    class_name = Column(String(50))
    enroll_year = Column(Integer)
    teacher_id = Column(Integer)
    invitation_code = Column(Integer)


class Notification(BaseModel):
    __tablename__ = 'notification'

    notification_id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    title = Column(String(100))
    date = Column(String(50))
    content = Column(Text)
    class_id = Column(Integer)
    allow_update = Column(Boolean)

    def is_allow_update(self):
        return self.allow_update


class Homework(BaseModel):
    __tablename__ = 'homework'

    homework_id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    title = Column(String(100))
    date = Column(String(50))
    course = Column(String(50))
    content = Column(Text)
    class_id = Column(Integer)
    allow_update = Column(Boolean)

    def is_allow_update(self):
        return self.allow_update