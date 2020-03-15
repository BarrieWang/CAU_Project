from util.util_mysql import *
from util.util_mysql import Users, UserCounts
from werkzeug.security import generate_password_hash, check_password_hash
import re
from uuid import uuid4


def checkuser(username, password, db):
    """
    :param username: 用户名
    :param password: 密码
    :param db: 数据库连接对象
    :return: 0：无用户名 1：密码不正确 用户数据库对象：登陆成功
    """
    ret = db.select(Users, Users.name == username)
    # ret=db.select_mysql(sql="select * from user where name = '"+username+"'")

    if not ret:
        return 0
    elif check_password_hash(ret[0].passwd, password) is False:
        return 1
    else:
        return ret[0]


def checkregister(username, password, repeatpasswd, useremail, captcha, db, cache):
    """
    :param username: 用户名
    :param password: 密码
    :param repeatpasswd: 重复密码
    :param useremail: 邮箱
    :param captcha: 验证码
    :param db: 数据库连接对象
    :param cache: 缓存对象
    :return: 0：用户名已被注册 1：密码不一致 2：邮箱格式有误 3：邮箱已被注册 4：验证码已超时 5：验证码错误 用户id：注册成功
    """
    emaillist = db.select(Users.email)
    namelist = db.select(Users.name)
    emaillist = [item[0] for item in emaillist]
    namelist = [item[0] for item in namelist]
    if username in namelist:
        return 0
    if password != repeatpasswd:
        return 1
    if re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', useremail) is None:
        return 2
    if useremail in emaillist:
        return 3
    if cache.get(useremail) is None:
        return 4
    if cache.get(useremail) != captcha:
        return 5
    userid = "U"+str(uuid4().hex)
    hashpasswd = generate_password_hash(password)
    userobj = Users(uid=userid, name=username, passwd=hashpasswd, email=useremail)
    usercount = UserCounts(uid=userid)
    db.insert(userobj)
    db.insert(usercount)
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
