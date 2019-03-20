#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# @Author  : Stevy
from flask import Blueprint


api_1_0 = Blueprint('api_1_0', __name__, url_prefix='/api')


from . import api_user, api_auth, api_sys
