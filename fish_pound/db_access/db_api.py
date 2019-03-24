#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Version : 1.0
# @Date    : 2018/11/04
# @Author  : PandaTofu

import copy
from contextlib import contextmanager

from sqlalchemy import and_
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from fish_pound.db_access.database import *
from fish_pound.utils import generate_hash


def singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton


@contextmanager
def get_db_session(db_url):
    engine = create_engine(db_url, encoding='utf-8', echo=True)
    session = scoped_session(sessionmaker(bind=engine))

    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


@singleton
class DbApi(object):
    def __init__(self):
        self.db_url = ''

    def init_app(self, app):
        app.db_api = self

        self.db_url = app.config.get('DB_URL', '')
        engine = create_engine(self.db_url, encoding='utf-8', echo=True)
        BaseModel.metadata.create_all(engine)



    def connect(self):
        return get_db_session(self.db_url)

    # -------------------Api for school table---------------------------
    def get_school(self, school_id):
        with self.connect() as db_session:
            return db_session.query(School).filter(School.school_id == school_id).first()

    def get_all_schools(self):
        with self.connect() as db_session:
            return db_session.query(School).all()

    def insert_school(self, **kwargs):
        with self.connect() as db_session:
            school = School(**kwargs)
            school.validate()
            db_session.add(school)

    def update_school(self, school_id, **kwargs):
        with self.connect() as db_session:
            school = db_session.query(School).filter(User.school_id == school_id).first()
            if school:
                school.update(kwargs)
                school.validate()

    def delete_school(self, school_id):
        with self.connect() as db_session:
            school = db_session.query(School).filter(User.school_id == school_id).first()
            if school:
                db_session.delete(school)

    # -------------------Api for user table---------------------------
    def get_user(self, phone_no):
        with self.connect() as db_session:
            user = db_session.query(User).filter(User.phone_no == phone_no).with_lockmode('read').first()
            return copy.deepcopy(user)

    def get_user_by_password(self, phone_no, password):
        encrypted_password = generate_hash(password)
        with self.connect() as db_session:
            user = db_session.query(User).\
                filter(and_(User.phone_no == phone_no, User.password == encrypted_password)).\
                with_lockmode('read').first()
            return copy.deepcopy(user)

    def insert_user(self, user):
        with self.connect() as db_session:
            user.validate()
            user.encrypt_password()
            db_session.add(user)

    def update_user(self, phone_no, **kwargs):
        with self.connect() as db_session:
            user = db_session.query(User).filter(User.phone_no == phone_no).with_lockmode('update').first()
            if user:
                user.update(kwargs)
                user.validate()
                user.encrypt_password()

    def delete_user(self, phone_no):
        with self.connect() as db_session:
            user = db_session.query(User).filter(User.phone_no == phone_no).with_lockmode('update').first()
            if user:
                db_session.delete(user)

    # -------------------Api for class table---------------------------
    def get_class(self, class_id):
        with self.connect() as db_session:
            class_record = db_session.query(Class).filter(Class.class_id == class_id).with_lockmode('read').first()
            return copy.deepcopy(class_record)

    def get_class_by_name_and_enroll_year(self, class_name, enroll_year):
        with self.connect() as db_session:
            class_record = db_session.query(Class).\
                filter(and_(Class.class_name == class_name, Class.enroll_year == enroll_year)).\
                with_lockmode('read').first()
            return copy.deepcopy(class_record)

    def get_classes_by_teacher_id(self, teacher_id):
        with self.connect() as db_session:
            class_records = db_session.query(Class).filter(Class.teacher_id == teacher_id).\
                with_lockmode('read').all()
            class_list = [db_class.data for db_class in class_records]
            return class_list

    def insert_class(self, class_record):
        class_name = class_record.class_name
        enroll_year = class_record.enroll_year
        with self.connect() as db_session:
            db_session.add(class_record)

        added_class = self.get_class_by_name_and_enroll_year(class_name, enroll_year)
        return added_class.class_id

    def update_class(self, class_id, **kwargs):
        with self.connect() as db_session:
            class_record = db_session.query(Class).filter(Class.class_id == class_id).with_lockmode('update').first()
            if class_record:
                class_record.update(kwargs)
                class_record.validate()

    def delete_class(self, class_id):
        with self.connect() as db_session:
            class_record = db_session.query(Class).filter(Class.class_id == class_id).with_lockmode('update').first()
            if class_record:
                db_session.delete(class_record)

    # -------------------Api for notification table---------------------------
    def get_notification(self, notification_id):
        with self.connect() as db_session:
            return db_session.query(Notification).filter(Notification.notification_id == notification_id).first()

    def get_notification_by_class_id(self, class_id):
        with self.connect() as db_session:
            return db_session.query(Notification).filter(Notification.class_id == class_id).all()

    def insert_notification(self, **kwargs):
        with self.connect() as db_session:
            notification = Notification(**kwargs)
            notification.validate()
            db_session.add(notification)

    def update_notification(self, notification_id, **kwargs):
        with self.connect() as db_session:
            notification = db_session.query(Notification).filter(Notification.notification_id == notification_id).first()
            if notification and notification.is_allow_update():
                notification.update(kwargs)
                notification.validate()

    def delete_notification(self, notification_id):
        with self.connect() as db_session:
            notification = db_session.query(Notification).filter(Notification.notification_id == notification_id).first()
            if notification:
                db_session.delete(notification)

    # -------------------Api for homework table---------------------------
    def get_homework(self, homework_id):
        with self.connect() as db_session:
            return db_session.query(Homework).filter(Homework.homework_id == homework_id).first()

    def get_homework_by_class_id(self, class_id):
        with self.connect() as db_session:
            return db_session.query(Homework).filter(Homework.class_id == class_id).all()

    def insert_homework(self, **kwargs):
        with self.connect() as db_session:
            homework = Homework(**kwargs)
            homework.validate()
            db_session.add(homework)

    def update_homework(self, homework_id, **kwargs):
        with self.connect() as db_session:
            homework = db_session.query(Homework).filter(Homework.homework_id == homework_id).first()
            if homework and homework.is_allow_update():
                homework.update(kwargs)
                homework.validate()

    def delete_homework(self, homework_id):
        with self.connect() as db_session:
            homework = db_session.query(Homework).filter(Homework.homework_id == homework_id).first()
            if homework:
                db_session.delete(homework)


