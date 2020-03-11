from util.util_mysql import UtilMysql, Questions, Answers, QuesCollections, AnsCollections, and_
from util.util_logging import *
from util.util_parameter import *


def delet_ans(aid, uid):
    """
    删除回答及其收藏
    :param aid:问题ID
    :param uid:用户ID
    :return state:删除操作状态
    """
    parameter = UtilParameter()
    logger = UtilLogging(parameter, False, False, False)
    db = UtilMysql(parameter.get_config("mysql"), logger)
    isOwner = db.select(Answers, and_(Answers.aid==aid, Answers.uid==uid))
    if len(isOwner) != 0:
        db.delete(AnsCollections, AnsCollections.aid == aid)
        db.delete(Answers, Answers.aid==aid)
        state = True
    else:
        state = False
    return state


def delet_ques(qid, uid):
    """
    删除问题函数
    :param qid:问题ID
    :param uid:用户ID
    :return: state:删除操作状态
    """
    parameter = UtilParameter()
    logger = UtilLogging(parameter, False, False, False)
    db = UtilMysql(parameter.get_config("mysql"), logger)
    isOwner = db.select(Questions, and_(Questions.qid == qid, Questions.uid==uid))
    if len(isOwner) != 0:
        flag = db.select(Answers.aid, Answers.qid==qid)
        flag1 = flag[0][0]
        db.delete(AnsCollections, and_(AnsCollections.aid==flag1))
        db.delete(Answers, Answers.qid==qid)
        db.delete(QuesCollections, QuesCollections.qid==qid)
        db.delete(Questions, Questions.qid==qid)
        state = True
    else:
        state = False
    return  state

