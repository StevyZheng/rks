#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# @Author  : Stevy


class Config:
	SECRET_KEY = '000000'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	MAIN_HOST = '0.0.0.0'
	MAIN_POST = 80
	
	@staticmethod
	def init_app(app):
		pass


class MySQLConfig:
	MYSQL_USERNAME = 'root'
	MYSQL_PASSWORD = '000000'
	MYSQL_HOST = '127.0.0.1'


class DevelopmentConfig(Config):
	DEBUG = True
	database = 'rks_dev'
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}'.format(MySQLConfig.MYSQL_USERNAME,
	                                                               MySQLConfig.MYSQL_PASSWORD,
	                                                               MySQLConfig.MYSQL_HOST, database)


class TestingConfig(Config):
	TESTING = True
	database = 'mysql_test'
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}'.format(MySQLConfig.MYSQL_USERNAME,
	                                                               MySQLConfig.MYSQL_PASSWORD,
	                                                               MySQLConfig.MYSQL_HOST, database)


class ProductionConfig(Config):
	database = 'rks_product'
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}'.format(MySQLConfig.MYSQL_USERNAME,
	                                                               MySQLConfig.MYSQL_PASSWORD,
	                                                               MySQLConfig.MYSQL_HOST, database)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
