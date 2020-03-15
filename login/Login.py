"""
author: 李润超
create time: 2020-03-4
update time: 2020-03-8
"""
from util.util_mysql import *
from werkzeug.security import generate_password_hash, check_password_hash
import re


def checkuser(username, password, db):
    """
    :param username: 用户名
    :param password: 密码
    :param db: 数据库连接对象
    :return: 0：无用户名 1：密码不正确 用户数据库对象：登陆成功
    """
    ret = db.select(Users, Users.name == username)
    # ret=db.select_mysql(sql="select * from user where name = '"+username+"'")
    if ret is False:
        return 0
    elif check_password_hash(ret[0].passwd, password) is False:
        return 1
    else:
        return ret[0]


def checkregister(username, password, repeatpasswd, useremail, db):
    """
    :param username: 用户名
    :param password: 密码
    :param repeatpasswd: 重复密码
    :param useremail: 邮箱
    :param db: 数据库连接对象
    :return: 0：用户名已被注册 1：密码不一致 2：邮箱格式有误 3：邮箱已被注册 用户id：注册成功
    """
    currenttable = db.select(Users)
    emaillist = []
    namelist = []
    for item in currenttable:
        emaillist.append(item.email)
        namelist.append(item.name)
    # print(emaillist)
    if username in namelist:
        return 0
    if password != repeatpasswd:
        return 1
    elif re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', useremail) is None:
        return 2
    elif useremail in emaillist:
        return 3
    else:

        idlist = []

        for item in currenttable:
            idlist.append(int(item.uid))
        # print(idlist)
        userid = str(max(idlist)+1)
        hashpasswd = generate_password_hash(password)
        print(len(hashpasswd), hashpasswd)
        userobj = Users(uid=userid, name=username, passwd=hashpasswd, email=useremail, authorization='0')
        db.insert(userobj)

        return userid


def storeinterest(interest, userid, db):
    """
    :param interest: 用户兴趣点编号，逗号隔开
    :param userid: 用户id
    :param db: 数据库连接对象
    :return: 1:存储完成
    """
    db.update(Users, {'labelset': interest}, Users.uid == userid)
    return 1
