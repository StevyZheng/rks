# !/usr/bin/env python
# encoding:utf-8
import inspect
import os
import re
import traceback
import random


def _init():
	global _global_dict
	_global_dict = {}


def _set_value(name, value):
	_global_dict[name] = value


def _get_value(name, defValue=None):
	try:
		return _global_dict[name]
	except KeyError:
		return defValue


class Debug(object):
	"""  调试及异常相关函数方法 """
	def __init__(self):
		pass
	
	@classmethod
	def get_class(cls, dist_cls):
		"""
		:param dist_cls: 目标类
        :return: 返回调用函数的类名
        """
		return dist_cls.__name__
	
	@classmethod
	def get_class_mod(cls, dist_cls):
		"""
        :param dist_cls: 目标类
        :return: 返回目标类中调用函数的模块全名
        """
		return dist_cls.__module__
	
	@classmethod
	def get_current_function_name(cls):
		"""
        :return: 返回当前的函数名
        """
		return inspect.stack()[1][3]
	
	@classmethod
	def get_except(cls, ex):
		"""
        :param ex: 异常变量
        :return: 返回要打印的异常字符串
        """
		return "exception msg:{0}{1}{0}traceback:{0}{2}".format(os.linesep, Exception(ex),
		                                                        traceback.format_exc())


class TextOp(object):
	def __init__(self):
		pass
	
	@classmethod
	def find_str(cls, src_str, reg_str, case=True, strip=True, reS=False):
		"""
        :param strip:
        :param src_str:
        :param reg_str:
        :param case: true upper lower, false not
        :return: list
        """
		if case:
			it = re.finditer(reg_str, src_str)
		else:
			it = re.finditer(reg_str, src_str, re.I)
		ret_list = []
		for match in it:
			if match is not None:
				if strip:
					ret_str = match.group().strip()
				else:
					ret_str = match.group()
				ret_list.append(ret_str)
		return ret_list
	
	@classmethod
	def find_str_column(cls, src_str, reg_str, column, split_str, case=True, strip=True):
		"""
        :param strip:
        :param src_str:
        :param reg_str:
        :param column: 列号
        :param split_str: 化分列的字符串
        :param case: true upper lower, false not
        :return: list
        """
		row_list = TextOp.find_str(src_str, reg_str, case, strip)
		ret_list = []
		for row_str in row_list:
			split_list = row_str.split(split_str)
			if len(split_list) > column:
				ret_list.append(split_list[column])
		return ret_list
	
	@classmethod
	def split_str(cls, src_str, split_str):
		if isinstance(src_str, str) and isinstance(split_str, str):
			ret_list = src_str.split(split_str)
			return ret_list
		else:
			return None


class Math(object):
	def __init__(self):
		pass
	
	@classmethod
	def random_matrix(cls, row, column):
		matrix = []
		for j in range(row):
			column_it = []
			for i in range(column):
				a = random.uniform(1, 10)
				column_it.append(a)
			matrix.append(column_it)
		return matrix
	
	@classmethod
	def solve_equations(cls):
		"""
        CPU、内存负载，单进程占一个线程，占497MB内存
        :return: 求得的方程解
        """
		matrix_a = Math.random_matrix(3800, 3800)
		matrix_b = Math.random_matrix(1, 3800)
		row_len = len(matrix_a)
		column_len = len(matrix_b[0])
		cross_len = len(matrix_b)
		res_mat = [[0] * row_len] * column_len
		while True:
			for i in range(row_len):
				for j in range(column_len):
					for k in range(cross_len):
						temp = matrix_a[i][k] * matrix_b[k][j]
						res_mat[i][j] += temp
