from util.util_mysql import UtilMysql, Questions, Answers, and_
from util.util_logging import *
from util.util_parameter import *


def query_content(uid, qid):
    '''
    查询问题内容函数
    :return:查询到的数据
    '''
    parameter = UtilParameter()
    logger = UtilLogging(parameter, False, False, False)
    db = UtilMysql(parameter.get_config("mysql"), logger)
    isOwner = db.select(Questions, and_(Questions.uid == uid, Questions.qid == qid))
    if len(isOwner) != 0:
        res = db.select(Questions, Questions.qid==qid)
        state = True
    else:
        res = None
        state = False
    return res, state

def updatq(uid, qid, label, title, content):
    """
    更新函数
    :param qid:问题ID
    :param label:问题类别
    :param content:问题内容
    :return state:更新状态
    """
    parameter = UtilParameter()
    logger = UtilLogging(parameter, False, False, False)
    db = UtilMysql(parameter.get_config("mysql"), logger)
    isOwner = db.select(Questions, and_(Questions.uid==uid, Questions.qid==qid))
    if len(isOwner) != 0:
        db.update(Questions, {Questions.label:label, Questions.ques_title:title, Questions.ques_content:content}, Questions.qid==qid)
        state = True
    else:
        state = False
    return state

