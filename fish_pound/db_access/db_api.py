#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Version : 1.0
# @Date    : 2018/11/04
# @Author  : PandaTofu


from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from db_access.database import School, User, Class, Notification, Homework


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


class DbApi(object):
    def __init__(self, db_url):
        self.db_url = db_url

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
            school.verify()
            db_session.add(school)

    def update_school(self, school_id, **kwargs):
        with self.connect() as db_session:
            school = db_session.query(School).filter(User.school_id == school_id).first()
            if school:
                school.update(kwargs)
                school.verify()

    def delete_school(self, school_id):
        with self.connect() as db_session:
            school = db_session.query(School).filter(User.school_id == school_id).first()
            if school:
                db_session.delete(school)

    # -------------------Api for user table---------------------------
    def get_user(self, phone_no):
        with self.connect() as db_session:
            return db_session.query(User).filter(User.phone_no == phone_no).first()

    def insert_user(self, **kwargs):
        with self.connect() as db_session:
            user = User(**kwargs)
            user.verify()
            db_session.add(user)

    def update_user(self, phone_no, **kwargs):
        with self.connect() as db_session:
            user = db_session.query(User).filter(User.phone_no == phone_no).first()
            if user:
                user.update(kwargs)
                user.verify()

    def delete_user(self, phone_no):
        with self.connect() as db_session:
            user = db_session.query(User).filter(User.phone_no == phone_no).first()
            if user:
                db_session.delete(user)

    # -------------------Api for class table---------------------------
    def get_class(self, class_id):
        with self.connect() as db_session:
            return db_session.query(Class).filter(Class.class_id == class_id).first()

    def get_classes_by_teacher_id(self, teacher_id):
        with self.connect() as db_session:
            return db_session.query(Class).filter(Class.teacher_id == teacher_id).all()

    def insert_class(self, **kwargs):
        with self.connect() as db_session:
            class_record = Class(**kwargs)
            class_record.verify()
            db_session.add(class_record)

    def update_class(self, class_id, **kwargs):
        with self.connect() as db_session:
            class_record = db_session.query(Class).filter(Class.class_id == class_id).first()
            if class_record:
                class_record.update(kwargs)
                class_record.verify()

    def delete_class(self, class_id):
        with self.connect() as db_session:
            class_record = db_session.query(Class).filter(Class.class_id == class_id).first()
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
            notification.verify()
            db_session.add(notification)

    def update_notification(self, notification_id, **kwargs):
        with self.connect() as db_session:
            notification = db_session.query(Notification).filter(Notification.notification_id == notification_id).first()
            if notification and notification.is_allow_update():
                notification.update(kwargs)
                notification.verify()

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
            homework.verify()
            db_session.add(homework)

    def update_homework(self, homework_id, **kwargs):
        with self.connect() as db_session:
            homework = db_session.query(Homework).filter(Homework.homework_id == homework_id).first()
            if homework and homework.is_allow_update():
                homework.update(kwargs)
                homework.verify()

    def delete_homework(self, homework_id):
        with self.connect() as db_session:
            homework = db_session.query(Homework).filter(Homework.homework_id == homework_id).first()
            if homework:
                db_session.delete(homework)