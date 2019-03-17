#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# @Author  : Stevy
import time
from app import db
from flask_restplus import Api, Resource
from flask import jsonify, request

from app.api_1_0 import api_1_0
from app.models.user import User
from app.api_1_0.api_auth import auth, generate_auth_token, verify_auth_token

api_user = Api(api_1_0)


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


class UserToken(Resource):
	# 返回一个token，默认是1个小时有限的token
	@auth.login_required
	def get(self):
		token = generate_auth_token(expiration=3600)
		return jsonify({'token': token.decode('ascii')})


api_user.add_resource(UserAddApi, '/useradd', endpoint='useradd')
api_user.add_resource(UserVerifyApi, '/userverify', endpoint='userverify')
api_user.add_resource(UserToken, '/usertoken', endpoint='usertoken')

