from util.util_mysql import UtilMysql, Questions, Answers, QuesCollections, AnsCollections, and_
from util.util_logging import *
from util.util_parameter import *


def delet_ans(uaid):
    """
    删除问题的所有回答
    :return:
    :param:uqid:问题ID
    """
    parameter = UtilParameter()
    logger = UtilLogging(parameter, False, False, False)
    db = UtilMysql(parameter.get_config("mysql"), logger)
    db.delete(AnsCollections, AnsCollections.aid == uaid)
    db.delete(Answers, Answers.aid==uaid)


def delet_ques(uqid):
    """
    删除问题函数
    :param uqid:问题ID
    :return: none
    """
    parameter = UtilParameter()
    logger = UtilLogging(parameter, False, False, False)
    db = UtilMysql(parameter.get_config("mysql"), logger)
    db.delete(AnsCollections, and_(Answers.aid==AnsCollections.aid, Answers.qid==uqid))
    db.delete(Answers, Answers.qid==uqid)
    db.delete(QuesCollections, QuesCollections.qid==uqid)
    db.delete(Questions, Questions.qid==uqid)

