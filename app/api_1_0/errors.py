#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# @Author  : Stevy
from . import api_1_0
from flask import jsonify, request, json
from werkzeug.exceptions import HTTPException
from rks import app


class BadRequest(Exception):
	"""将本地错误包装成一个异常实例供抛出"""
	def __init__(self, message, status=400, payload=None):
		self.message = message
		self.status = status
		self.payload = payload


class ApiException(HTTPException):
	code = 500
	msg = 'sorry, we make a mistake'
	error_code = 999
	
	def __init__(self, code=None, msg=None, error_code=None, header=None):
		if code:
			self.code = code
		if msg:
			self.msg = msg
		if error_code:
			self.error_code = error_code
		super(ApiException, self).__init__(msg, None)
	
	def get_body(self, environ=None):
		body = dict(
			msg=self.msg,
			error_code=self.error_code,
			# 形如request="POST v1/client/register"
			request=request.method + ' ' + self.get_url_no_param()
		)
		text = json.dumps(body)
		return text
	
	def get_headers(self, environ=None):
		return [('Content-Type', 'application/json')]
	
	@staticmethod
	def get_url_no_param():
		full_url = str(request.full_path)
		main_path = full_url.split('?')
		return main_path[0]


class Success(ApiException):
	code = 200
	msg = "success"
	error_code = 0


class UserException(ApiException):
	code = 201
	msg = "用户名不可为空"
	error_code = 50000


@api_1_0.app_errorhandler(Exception)
def handle_bad_request(e):
	"""捕获 ApiExcetion、HttpException、Exception全局异常，序列化为 JSON 并返回 HTTP 400"""
	if isinstance(e, ApiException):
		return e
	if isinstance(e, HTTPException):
		code = e.code
		msg = e.description
		error_code = 1007
		return ApiException(code=code, msg=msg, error_code=error_code)
	else:
		from flask import current_app
		if not current_app.config['development']:
			return ApiException()
		raise e







