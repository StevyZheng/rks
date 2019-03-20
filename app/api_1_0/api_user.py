#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# @Author  : Stevy
import time
from app import db
from flask_restplus import Api, Resource, reqparse
from flask import jsonify, request

from app.api_1_0 import api_1_0
from app.models.user import User, Role
from app.api_1_0.api_auth import auth, generate_auth_token, verify_auth_token

api_user = Api(api_1_0)
user_parser = api_user.parser()
user_parser.add_argument('username', location=['json', 'args'], type=str, required=False)
user_parser.add_argument('role', location=['json', 'args'], type=str, required=False)


@api_user.route('/userlist', endpoint='userlist')
class UserListApi(Resource):
	@auth.login_required
	def get(self):
		user_info = request.get_json()
		try:
			args = user_parser.parse_args()
			username_agr = args['username']
			role_arg = args['role']
			if username_agr is not None and role_arg is None:
				us = User.query.filter(User.username == username_agr)
			elif username_agr is not None and role_arg is not None:
				us = User.query.join(Role).filter(User.username == username_agr, Role.rolename == role_arg)
			elif username_agr is None and role_arg is not None:
				us = User.query.join(Role).filter(Role.rolename == role_arg)
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


@api_user.route('/useradd', endpoint='useradd')
class UserAddApi(Resource):
	@auth.login_required
	def post(self):
		user_info = request.get_json()
		try:
			u = User(username=user_info['username'])
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


@api_user.route('/userverify', endpoint='userverify')
class UserVerifyApi(Resource):
	# 根据传过来的账号密码，返回验证结果。
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


@api_user.route('/usertoken', endpoint='usertoken')
class UserToken(Resource):
	# 返回一个token，默认是1个小时有限的token
	@auth.login_required
	def get(self):
		token = generate_auth_token(expiration=3600)
		return jsonify({'token': token.decode('ascii')})


# api_user.add_resource(UserAddApi, '/useradd', endpoint='useradd')
# api_user.add_resource(UserVerifyApi, '/userverify', endpoint='userverify')
# api_user.add_resource(UserToken, '/usertoken', endpoint='usertoken')
# api_user.add_resource(UserListApi, '/userlist', endpoint='userlist')

