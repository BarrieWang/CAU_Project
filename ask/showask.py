from util.util_mysql import UtilMysql, Questions, Answers, QuesCollections, AnsCollections
from util.util_logging import *
from util.util_parameter import *


def query(uuid, uqid, ulabel):
    '''
    查询函数
    :param uuid:用户ID
    :param uqid:问题ID
    :param ulabel:问题标签
    :return:查询到全部数据
    '''
    parameter = UtilParameter()
    logger = UtilLogging(parameter, False, False, False)
    db = UtilMysql(parameter.get_config("mysql"), logger)
    if uuid is None and ulabel is None and uqid is None:
        res = db.select(Questions)
        return res
    elif uuid is not None:
        res = db.select(Questions, Questions.uid==uuid)
        return res
    elif ulabel is not None:
        res = db.select(Questions, Questions.label==ulabel)
        return res


def queryCQ(uid):
    """
    查询用户收藏问题
    :param uid: 用户ID
    :return: 问题对象列表
    """
    parameter = UtilParameter()
    logger = UtilLogging(parameter, False, False, False)
    db = UtilMysql(parameter.get_config("mysql"), logger)
    tem = db.select(QuesCollections.qid, QuesCollections.uid==uid)
    list = []
    for each in tem:
        list.append(each[0])
    res = db.select(Questions, Questions.qid.in_(list))
    return res


def queryCA(uid):
    """
    查询用户收藏答案
    :param uid: 用户ID
    :return: 回答对象列表
    """
    parameter = UtilParameter()
    logger = UtilLogging(parameter, False, False, False)
    db = UtilMysql(parameter.get_config("mysql"), logger)
    tem = db.select(AnsCollections.aid, AnsCollections.uid == uid)
    list = []
    for each in tem:
        list.append(each[0])
    res = db.select(Answers, Answers.aid.in_(list))
    return res

