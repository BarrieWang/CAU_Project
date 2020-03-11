from util.util_mysql import UtilMysql, Questions, Answers
from util.util_logging import *
from util.util_parameter import *
import datetime
import uuid


def to_show_details(uqid):
    """
    查询问题及其答案
    :param uqid: 问题ID
    :return: 查询到的问题及其答案
    """
    parameter = UtilParameter()
    logger = UtilLogging(parameter, False, False, False)
    db = UtilMysql(parameter.get_config("mysql"), logger)
    ques = db.select(Questions, Questions.qid == uqid)[0]
    ans = db.select(Answers, Answers.qid == uqid)
    return ques, ans


def to_answer(uid, qid, acontent, nameflag):
    """
    建立回答
    :param uuid:回答用户ID
    :param uqid: 回答问题ID
    :param acontent: 回答内容
    :return:
    """
    parameter = UtilParameter()
    logger = UtilLogging(parameter, False, False, False)
    db = UtilMysql(parameter.get_config("mysql"), logger)
    aid = 'A' + uuid.uuid4().hex
    if nameflag == 'on':
        noname = True
    else:
        noname = False
    answer = Answers(aid=aid, uid=uid, qid=qid, ans_content=acontent, ans_anonymous=noname)
    db.insert(answer)