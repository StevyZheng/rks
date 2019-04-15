#!/usr/bin/env python
# encoding:utf-8
from .rks_exception import *
import paramiko


class RksParamiko:
	def __init__(self, host_ip, username, password, port=22):
		self.host_ip = host_ip
		self.port = port
		self.username = username
		self.password = password
		self.obj = paramiko.SSHClient()
		self.obj.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		try:
			self.obj.connect(self.host_ip, self.port, self.username, self.password)
			self.obj_sftp = self.obj.open_sftp()
		except Exception:
			raise RksException(code=100, message=err_msg[1], args=(err_msg[1],))
	

