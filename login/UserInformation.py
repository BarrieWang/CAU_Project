from util.util_mysql import *
import os


def get_user(uid, db):
    """
    得到用户信息
    :param uid: 用户id
    :param db: 数据库连接对象
    :return: 用户数据库类
    """
    ret = db.select(Users, Users.uid == uid)
    return ret[0]


def get_avatar(uid):
    """
    得到用户头像地址
    :param uid: 用户id
    :return: 用户头像地址
    """

    sep = '\\'   # 玮韬，linux里这里要改成'/'

    path = os.path.dirname(os.path.realpath(__file__)).split(sep)
    path.pop()
    pathstr = str()
    for i in range(len(path)):
        pathstr = pathstr + path[i] + sep
    pathstr += 'static' + sep + 'images' + sep
    for i in os.listdir(pathstr):
        if i.split('.')[0] == uid:
            break
    if i.split('.')[0] == uid:
        pathstr = sep + 'static' + sep + 'images' + sep + i
        return pathstr
    else:
        pathstr = sep + 'static' + sep + 'images' + sep + 'avatar.jpg'    # 返回默认头像
        return pathstr


def changeimage(uid, f):
    """
    删除原来的图片，保存新的图片
    :param uid: 用户id
    :param f: 图片
    :return: -1：图片不存在 0：图片格式不支持 1：更改完成
    """
    # 允许格式
    allowed_extensions = ['png', 'jpg', 'jpeg', 'gif']
    # 后缀名
    if f is None:
        return -1
    else:
        ext = f.filename
        fext = ext.split('.')[1]
        if fext not in allowed_extensions:
            return 0
        else:
            sep = '\\'         # 玮韬，linux里这里要改成'/'
            path = os.path.dirname(os.path.realpath(__file__)).split(sep)
            path.pop()
            pathstr = str()
            for i in range(len(path)):
                pathstr = pathstr + path[i] + sep
            pathstr += sep + 'static' + sep + 'images' + sep
            for i in os.listdir(pathstr):
                print(i)
                if i.split('.')[0] == uid:
                    os.remove(pathstr + i)
            newpath = pathstr + uid + '.' + fext
            f.save(newpath)
            return 1
