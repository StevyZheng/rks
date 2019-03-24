#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# @Author  : Stevy
import time
from enum import Enum
from app import db
from flask_restplus import Api, Resource
from flask import jsonify, request

from app.api_1_0 import api_1_0
from app.models.user import User, Role
from app.api_1_0.api_auth import auth, generate_auth_token, verify_auth_token
from .errors import *

api = Api(api_1_0)


class RoleName(Enum):
	ADMIN = "admin"
	NORMAL = "normal"


@api.route('/userlist', endpoint='userlist')
class UserListApi(Resource):
	@auth.login_required
	def get(self):
		user_info = request.get_json()
		user_info_keys = user_info.keys()
		try:
			if 'username' in user_info_keys and 'role' in user_info_keys:
				us = User.query.join(Role).filter(User.username == user_info['username'],
				                                  Role.rolename == user_info['role'])
			elif 'username' not in user_info_keys and 'role' in user_info_keys:
				us = User.query.join(Role).filter(Role.rolename == user_info['role'])
			elif 'username' in user_info_keys and 'role' not in user_info_keys:
				us = User.query.filter(User.username == user_info['username'])
			else:
				us = User.query.all()
		except Exception as ex:
			print("{} User query: failure...{}".format(time.strftime("%Y-%m-%d %H:%M:%S"), ex))
			return False
		else:
			print("{} User query: success...".format(time.strftime("%Y-%m-%d %H:%M:%S")))
			ret = []
			for it in us:
				ret.append(it.to_json())
			return jsonify(ret)
		finally:
			db.session.close()


@api.route('/useradd', endpoint='useradd')
class UserAddApi(Resource):
	"""
	accpet json: {username: str, password: str, role: str}
	username必须有，password和role默认值为000000和normal
	"""
	
	@auth.login_required
	def post(self):
		user_info = request.get_json()
		if 'username' not in user_info.keys():
			raise UserException(msg="用户名不能为空")
		if 'password' not in user_info.keys():
			user_info['password'] = "000000"
		if 'role' not in user_info.keys():
			rs = Role.query.filter(Role.rolename == RoleName.NORMAL).first()
			user_info['role'] = rs.id
		try:
			u = User(username=user_info['username'], password=user_info['password'], role=user_info['role'])
			if u is None or u.verify_password(user_info['password']) is False:
				print("{} User query: {} failure...".format(time.strftime("%Y-%m-%d %H:%M:%S"), user_info['username']))
				return False
			db.session.add(u)
			db.session.commit()
		except Exception as ex:
			print(
				"{} User insert: {} failure...{}".format(time.strftime("%Y-%m-%d %H:%M:%S"), user_info['username'], ex))
			return False
		
		else:
			print("{} User insert: {} success...".format(time.strftime("%Y-%m-%d %H:%M:%S"), user_info['username']))
			return True
		finally:
			db.session.close()


@api.route('/userdel', endpoint='userdel')
class UserDelApi(Resource):
	"""
	:param json {username}
	"""
	@auth.login_required
	def post(self):
		user_info = request.get_json()
		try:
			u = User.query.filter_by(username=user_info["username"])
			if u is None:
				raise UserException(msg="该用户不存在")
			else:
				db.session.delete(u[0])
				db.session.commit()
		except Exception as ex:
			print(
				"{} User delete: {} failure...{}".format(time.strftime("%Y-%m-%d %H:%M:%S"), user_info['username'], ex))
		else:
			print(
				"{} User delete: {} success...".format(time.strftime("%Y-%m-%d %H:%M:%S"), user_info['username']))
		finally:
			db.session.close()


@api.route('/userupdate', endpoint='userupdate')
class UserUpdateApi(Resource):
	"""
	:param json {username: str, password: str, role: str}
	"""
	
	@auth.login_required
	def post(self):
		user_info = request.get_json()
		keys = user_info.keys()
		if 'username' not in keys:
			raise UserException(msg="用户名不能为空")
		update_dict = {}
		if 'password' in keys and 'role' in keys:
			update_dict['password'] = user_info['password']
			update_dict['role'] = user_info['role']
		elif 'password' in keys and 'role' not in keys:
			update_dict['password'] = user_info['password']
		elif 'password' not in keys and 'role' in keys:
			update_dict['role'] = user_info['role']
		else:
			raise UserException(202, "没有给出password或role值", 50001)
		User.query.filter_by(username=user_info['username']).update(update_dict)


@api.route('/userverify', endpoint='userverify')
class UserVerifyApi(Resource):
	"""
	根据传过来的账号密码，返回验证结果。
	:param json {username, password}
	"""
	@auth.login_required
	def post(self):
		user_info = request.get_json()
		try:
			u = User.query.filter_by(username=user_info['username']).first()
			if u is None or u.verify_password(user_info['password']) is False:
				print("{} User query: {} failure...".format(time.strftime("%Y-%m-%d %H:%M:%S"), user_info['username']))
				return False
		except:
			print("{} User query: {} failure...".format(time.strftime("%Y-%m-%d %H:%M:%S"), user_info['username']))
			return False
		else:
			print("{} User query: {} success...".format(time.strftime("%Y-%m-%d %H:%M:%S"), user_info['username']))
			return True
		finally:
			db.session.close()


@api.route('/usertoken', endpoint='usertoken')
class UserToken(Resource):
	""" 返回一个token，默认是1个小时有限的token """
	@auth.login_required
	def get(self):
		token = generate_auth_token(expiration=3600)
		return jsonify({'token': token.decode('ascii')})

# api_user.add_resource(UserAddApi, '/useradd', endpoint='useradd')
# api_user.add_resource(UserVerifyApi, '/userverify', endpoint='userverify')
# api_user.add_resource(UserToken, '/usertoken', endpoint='usertoken')
# api_user.add_resource(UserListApi, '/userlist', endpoint='userlist')
