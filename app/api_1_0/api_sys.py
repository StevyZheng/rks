#!/usr/bin/env python
# encoding:utf-8
from flask_restplus import Api, Resource, reqparse
from flask import jsonify, request

from app.api_1_0.api_user import api_user as api_sys
from app.api_1_0.api_auth import auth, generate_auth_token, verify_auth_token
from libs.sys import Sys


@api_sys.route('/sysinfo', endpoint='sysinfo')
class SysinfoApi(Resource):
	@auth.login_required
	def get(self):
		try:
			return {
				"cpu": Sys.get_cpu_info(),
				"memory": Sys.get_mem_info()
			}
		except Exception as ex:
			print(ex)

