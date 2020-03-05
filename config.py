# -*- coding: utf-8 -*-
# @Author  : Chicker
# @FileName: config.py
# @Software: PyCharm
# @Blog    ：https://blog.csdn.net/weixin_44310290


# 数据库配置文件 这里的例子是按照mysql配置的
# 若有需要可以套用mysql用这个文件修改即可，注意要配置好数据库驱动

import os

SECRET_KEY = os.urandom(24)
DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'guest'
PASSWORD = 'Guestpass1!'
HOST = '47.93.56.66'
PORT = '3306'
DATABASE = 'CAU_Project'
SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False
