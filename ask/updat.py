from util.util_mysql import UtilMysql, Questions, Answers, and_
from util.util_logging import *
from util.util_parameter import *


def query_qcontent(uid, qid):
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
    更新问题函数
    :param uid:用户ID
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
        db.update(Questions, {Questions.label:label, Questions.ques_title:title, Questions.ques_content:content, Questions.ques_time:datetime.datetime.now()}, Questions.qid==qid)
        state = True
    else:
        state = False
    return state


def query_acontent(uid, aid):
    '''
    查询回答及其对应问题函数
    :return:查询到的数据
    '''
    parameter = UtilParameter()
    logger = UtilLogging(parameter, False, False, False)
    db = UtilMysql(parameter.get_config("mysql"), logger)
    isOwner = db.select(Answers, and_(Answers.uid == uid, Answers.aid == aid))
    if len(isOwner) != 0:
        qid = db.select(Answers.qid, Answers.aid==aid)
        qres = db.select(Questions, Questions.qid==qid[0][0])
        ares = db.select(Answers, Answers.aid==aid)
        state = True
    else:
        qres = None
        ares = None
        state = False
    return qres, ares, state


def updata(uid, aid, content):
    """
    更新回答函数
    :param uid:用户ID
    :param aid:回答ID
    :param content:回答内容
    :return state:更新状态
    """
    parameter = UtilParameter()
    logger = UtilLogging(parameter, False, False, False)
    db = UtilMysql(parameter.get_config("mysql"), logger)
    isOwner = db.select(Answers, and_(Answers.aid==aid, Answers.uid==uid))
    if len(isOwner) != 0:
        db.update(Answers, {Answers.ans_content:content, Answers.ans_time:datetime.datetime.now()}, Answers.aid==aid)
        state = True
    else:
        state = False
    return state

