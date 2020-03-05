# -*- coding: utf-8 -*-
from functools import wraps
from flask import session,redirect,url_for
# define a func to limit some function if you don't login
# 限制必须要登陆才可以发表评论的功能：python 装饰器


def login_limit(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if session.get('user_id'):
            return func(*args,**kwargs)
        else:
            return redirect(url_for('yy_login'))
    return wrapper
