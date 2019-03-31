#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Version : 1.0
# @Date    : 2018/11/04
# @Author  : PandaTofu

import copy

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, Boolean, Enum, ForeignKey, relationship, backref
from sqlalchemy.dialects.mysql import INTEGER
from fish_pound.db_access.constants import AccountType
from fish_pound.utils import generate_hash

BaseModel = declarative_base()


class BaseModel(BaseModel):
    __abstract__ = True

    def validate(self):
        return True

    def update(self, attrs):
        for key, value in attrs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    @property
    def data(self):
        data_dict = self.__dict__
        data_dict.pop('_sa_instance_state')
        return copy.deepcopy(data_dict)


class School(BaseModel):
    __tablename__ = 'school'

    school_id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    school_name = Column(String(50))
    address = Column(String(100))


class ClassRoom(BaseModel):
    __tablename__ = 'class_room'

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    enroll_year = Column(Integer, nullable=False)
    invitation_code = Column(String(32), unique=True)
    head_teacher_id = Column(Integer, nullable=False)


class User(BaseModel):
    __tablename__ = u'user'

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    phone_no = Column(String(20), unique=True, nullable=True)
    password = Column(String(50), nullable=False)
    account_type = Column(Enum(AccountType), nullable=False)
    nick_name = Column(String(50), unique=True)
    school_id = Column(Integer)
    teacher_cert_id = Column(Integer, unique=True)
    activated = Column(Boolean, default=False)
    class_room_id = Column(Integer, ForeignKey('class_room.id'))
    class_room = relationship('ClassRoom', backref=backref('members', order_by=id))

    def validate(self):
        if self.account_type == AccountType.teacher.name and self.teacher_id is None:
            raise ValueError("No teacher_id for user[%s]" % self.phone_no)

    def encrypt_password(self):
        if self.password is None:
            return

        password_hash = generate_hash(self.password)
        self.update({"password": password_hash})

    def verify_password(self, compare_password):
        compare_password_hash = generate_hash(compare_password)
        return compare_password_hash == self.password

    def get_id(self):
        return self.id

    @property
    def roles(self):
        return [self.account_type]

    @property
    def is_active(self):
        return self.activated

    @property
    def is_authenticated(self):
        # if not anonymous user, authenticated = True
        return True

    @property
    def is_anonymous(self):
        return False


class Notification(BaseModel):
    __tablename__ = 'notification'

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    title = Column(String(100))
    date = Column(String(50))
    content = Column(Text)
    class_id = Column(Integer)
    allow_update = Column(Boolean)


class Homework(BaseModel):
    __tablename__ = 'homework'

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    title = Column(String(100))
    date = Column(String(50))
    course = Column(String(50))
    content = Column(Text)
    class_id = Column(Integer)
    allow_update = Column(Boolean)

    def is_allow_update(self):
        return self.allow_update


