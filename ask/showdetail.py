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


def to_answer(uid, qid, acontent):
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
    print(aid)
    uans_time = datetime.datetime.now()
    uans_collect = 0
    answer = Answers(aid=aid, uid=uid, qid=qid, ans_content=acontent)
    # answer = Answers(aid=uaid, uid=uuid, qid=uqid, ans_content=acontent, ans_time=uans_time, ans_collect=uans_collect)
    print(answer)
    db.insert(answer)