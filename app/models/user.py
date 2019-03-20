#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# @Author  : Stevy
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class Role(db.Model):
	__tablename__ = 'role'
	id = db.Column(db.Integer, primary_key=True)
	rolename = db.Column(db.String(64), unique=True, index=True)


class User(db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, index=True)
	password_hash = db.Column(db.String(128))
	role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
	# role = db.relationship('Role', backref=db.backref('users'), lazy='dynamic')
	role = db.relationship('Role', backref=db.backref('users'), lazy='subquery')
	
	def __init__(self, username, password, role='normal'):
		self.username = username
		self.password = password
		if role is not None:
			self.role = Role.query.filter_by(rolename=role).first()
		else:
			self.role = Role.queryy.filter_by(rolename='normal').first()
	
	@property
	def password(self):
		raise AttributeError('password is not readable attribute')
	
	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)
	
	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)
	
	def __repr__(self):
		return "<User {}>".format(self.username)
	
	def to_json(self):
		return {
			'id': self.id,
			'username': self.username,
			'password_hash': self.password_hash,
			'role': self.role.rolename
		}

