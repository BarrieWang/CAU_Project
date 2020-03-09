from util.util_mysql import UtilMysql, Questions, Answers
from util.util_logging import *
from util.util_parameter import *


def delet_ans(uid, uqid, uaid):
    """
    删除问题的所有回答
    :return:
    :param:uqid:问题ID
    """
    parameter = UtilParameter()
    logger = UtilLogging(parameter, False, False, False)
    db = UtilMysql(parameter.get_config("mysql"), logger)
    if uid is not None:
        db.delete(Answers, Answers.uid==uid)
    elif uqid is not None:
        db.delete(Answers, Answers.qid==uqid)
    elif uaid is not None:
        db.delete(Answers, Answers.aid==uaid)
    else:
        print("Delete Nothing")


def delet_ques(uid, uqid):
    """
    删除问题函数
    :param uqid:问题ID
    :return: none
    """
    parameter = UtilParameter()
    logger = UtilLogging(parameter, False, False, False)
    db = UtilMysql(parameter.get_config("mysql"), logger)
    if uid is not None:
        db.delete(Answers, Answers.uid==uid)
        db.delete(Questions, Questions.uid==uid)
    elif uqid is not None:
        db.delete(Answers, Answers.qid==uqid)
        db.delete(Questions, Questions.qid==uqid)

