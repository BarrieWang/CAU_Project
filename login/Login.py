from util.util_mysql import *
from util.util_logging import *
from util.util_parameter import *
import re
def CheckUser(username,password):
    """
    :param username: 用户名
    :param password: 密码
    :return: 0：无用户名 1：密码不正确 result：登陆成功
    """
    parameter=UtilParameter()
    logger=UtilLogging(parameter, False, False, False)

    db=UtilMysql(parameter.get_config("mysql"),logger)
    #print(type(Users.name==username))
    ret=db.select(Users,Users.name==username)
    #ret=db.select_mysql(sql="select * from user where name = '"+username+"'")

    #print(ret[0].passwd)
    #print(password)
    if(ret ==[]):
        return 0
    elif(ret[0].passwd!=password):
        return 1
    else:
        return ret

def CheckRegister(username,password,repeatpasswd,useremail):
    """

    :param username: 用户名
    :param password: 密码
    :param repeatpasswd: 重复密码
    :param useremail: 邮箱
    :return: 0：密码不一致 1：邮箱格式有误，2：邮箱已被注册，3：注册成功
    """
    parameter = UtilParameter()
    logger = UtilLogging(parameter, False, False, False)
    db = UtilMysql(parameter.get_config("mysql"), logger)
    CurrentTable = db.select(Users)
    emaillist=[]
    namelist=[]
    for item in CurrentTable:
        emaillist.append(item.email)
        namelist.append(item.name)
    #print(emaillist)
    if(username in namelist):
        return 0
    if(password!=repeatpasswd):
        return 1
    elif(re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$',useremail) is None):
        return 2
    elif(useremail in emaillist):
        return 3
    else:

        idlist=[]

        for item in CurrentTable:
            idlist.append(int(item.uid))
        print(idlist)
        userobj=Users(uid=str(max(idlist)+1),name=username,passwd=password,email=useremail)
        db.insert(userobj)

        return 4
