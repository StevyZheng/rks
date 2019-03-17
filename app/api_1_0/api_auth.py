#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# @Author  : Stevy
from flask_httpauth import HTTPBasicAuth
from flask import jsonify, app
from itsdangerous import SignatureExpired, BadSignature
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from config import Config

from app.models.user import User

auth = HTTPBasicAuth()


# 请求api接口数据的时候，-u 后面输入的账号密码不正确，返回该值
@auth.error_handler
def unauthorized():
    error_info = '{}'.format("Invalid credentials")
    print(error_info)
    response = jsonify({'error': error_info})
    response.status_code = 403
    return response


# 只是一个辅助函数，当传入用户名密码的时候，查询数据库中是否有这条记录
# 并且密码也正确，则返回为True
def verify_password_for_token(username, password):
    user = User.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    return True


# 验证 token 和 用户名密码
# 默认传的用户名密码的格式，例如用户名叫liuxin，密码是123456 在shell里加入 -u username:password
# 先验证用户名，首先假想是token，解密，查询是否有这么个用户存在，如果有返回True
# 如果用户名，那么上面解密这个名字，也肯定解密不出来，所以得出来的user是None
# 那么接下来就通过用户名密码的方式验证
# 需要注意的是，传入token的方式与传账号密码的方式一样，别忘记后面加一个冒号:
# url中加入@auth.login_required修饰符，会默认调用此函数
@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = verify_auth_token(username_or_token)
    if user is None:
        # try to authenticate with username/password
        return verify_password_for_token(username=username_or_token, password=password)
    return True


# 定义一个产生token的方法
def generate_auth_token(expiration=36000):
    # 注意这里的Serializer是这么导入的
    # from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
    s = Serializer(secret_key=Config.SECRET_KEY, expires_in=expiration)
    # print(s.dumps({'id': 1}))
    # 返回第一个用户，这里我就将数据库里的id=1的用户作为token的加密用户
    return s.dumps({'id': 1})


# 解密token，因为上面加密的是 id=1 的用户，所以解密出来的用户也是 id=1 的用户
# 所以data的数值应该是 {'id': 1}
def verify_auth_token(token):
    s = Serializer(Config.SECRET_KEY)
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None  # valid token, but expired
    except BadSignature:
        return None  # invalid token
    user = User.query.get(data['id'])
    return user

