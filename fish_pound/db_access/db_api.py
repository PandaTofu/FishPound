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
from fish_pound.utils import generate_hash, singleton


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
    def get_user_by_phone_no(self, phone_no=None):
        with self.connect() as db_session:
            user = db_session.query(User).filter(User.phone_no == phone_no).with_lockmode('read').first()
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
    def get_class_room(self, class_id):
        with self.connect() as db_session:
            class_room = db_session.query(ClassRoom).\
                filter(ClassRoom.id == class_id).with_lockmode('read').first()
            return copy.deepcopy(class_room)

    def get_class_room_by_name_and_enroll_year(self, name, enroll_year):
        with self.connect() as db_session:
            class_room = db_session.query(ClassRoom).\
                filter(and_(ClassRoom.name == name, ClassRoom.enroll_year == enroll_year)).\
                with_lockmode('read').first()
            return copy.deepcopy(class_room)

    def get_class_rooms_by_head_teacher(self, head_teacher_id):
        with self.connect() as db_session:
            class_rooms = db_session.query(ClassRoom).filter(ClassRoom.head_teacher_id == head_teacher_id).\
                with_lockmode('read').all()
            class_room_list = [db_class.data for db_class in class_rooms]
            return class_room_list

    def get_class_room_by_invitation_code(self, invitation_code):
        with self.connect() as db_session:
            class_room = db_session.query(ClassRoom).\
                filter(ClassRoom.invitation_code == invitation_code).with_lockmode('read').first()
            return copy.deepcopy(class_room)

    def insert_class_room(self, class_room):
        name = class_room.name
        enroll_year = class_room.enroll_year
        with self.connect() as db_session:
            db_session.add(class_room)

        added_class = self.get_class_by_name_and_enroll_year(name, enroll_year)
        return added_class.class_id

    def update_class_room(self, class_id, **kwargs):
        with self.connect() as db_session:
            class_room = db_session.query(ClassRoom).\
                filter(ClassRoom.id == class_id).with_lockmode('update').first()
            if class_room:
                class_room.update(kwargs)
                class_room.validate()

    def delete_class_room(self, class_id):
        with self.connect() as db_session:
            class_room = db_session.query(ClassRoom).filter(ClassRoom.id == class_id).with_lockmode('update').first()
            if class_room:
                db_session.delete(class_room)

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

    # -------------------Api for class_room-user relationship table---------------------------
    def join_class_room(self, user_id, invitation_code):
        with self.connect() as db_session:
            user = db_session.query(User).filter(User.id == user_id).with_lockmode('read').first()
            class_room = db_session.query(ClassRoom).\
                filter(ClassRoom.invitation_code == invitation_code).with_lockmode('read').first()
            user.class_room = class_room
