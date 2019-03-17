#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# @Author  : Stevy
from app import create_app


def init_db(mysql_db='default'):
    from app.models.user import User
    from app import db
    app = create_app(mysql_db)
    app.app_context().push()
    db.drop_all()
    db.create_all()
    db.session.commit()


init_db()
