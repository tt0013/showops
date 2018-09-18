#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Yang Tian Qi

from flask import Flask
import pymysql
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:sinashow@192.168.9.126:3306/CMDB'

app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)


class usersalt(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    user = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(50), unique=True)

    __tablename__ = 'salt_user'

    def __init__(self, id=None, user=None, password=None):
        self.id = id
        self.user = user
        self.password = password


    def __repr__(self):
        return '<User %r>' % self.name



# db.create_all()
# inset = usersalt(user="salt", password="saltstack")
# db.session.add(inset)
# db.session.commit()
