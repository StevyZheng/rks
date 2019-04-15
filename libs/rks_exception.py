#!/usr/bin/env python
# encoding:utf-8

err_msg = {
	1: "ssh init error: connect or open_sftp failed",
	2: ""
}


class RksException(Exception):
	def __init__(self, code=100, message="", *args):
		self.code = code
		self.message = message
		self.args = args


