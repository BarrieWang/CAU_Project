import uuid
from util.util_mysql import UtilMysql, QuesCollections, AnsCollections, Questions, Answers, and_
from util.util_logging import *
from util.util_parameter import *


def to_collect_ques(uid, qid):
    """
    收藏问题
    :param uid:用户ID
    :param qid: 问题ID
    :return:
    """
    parameter = UtilParameter()
    logger = UtilLogging(parameter, False, False, False)
    db = UtilMysql(parameter.get_config("mysql"), logger)
    isCollected = db.select(QuesCollections, and_(QuesCollections.qid==qid, QuesCollections.uid==uid))
    # 判断是否已经收藏
    if len(isCollected) != 0:
        print("You have already collected!")
    else:
        cid = 'C' + uuid.uuid4().hex
        db.update(Questions, {Questions.ques_collect: Questions.ques_collect+1}, Questions.qid==qid)
        quesCollection = QuesCollections(cid=cid, uid=uid, qid=qid)
        db.insert(quesCollection)


def to_collect_ans(uid, aid):
    """
    收藏回答
    :param uid:用户ID
    :param aid: 回答ID
    :return:
    """
    parameter = UtilParameter()
    logger = UtilLogging(parameter, False, False, False)
    db = UtilMysql(parameter.get_config("mysql"), logger)
    isCollected = db.select(AnsCollections, and_(AnsCollections.aid == aid, AnsCollections.uid == uid))
    # 判断是否已经收藏
    if len(isCollected) != 0:
        print("You have already collected!")
    else:
        cid = 'C' + uuid.uuid4().hex
        db.update(Answers, {Answers.ans_collect: Answers.ans_collect + 1}, Answers.aid == aid)
        ansCollextion = AnsCollections(cid=cid, uid=uid, aid=aid)
        db.insert(ansCollextion)


def to_cancel_collectq(qid, uid):
    parameter = UtilParameter()
    logger = UtilLogging(parameter, False, False, False)
    db = UtilMysql(parameter.get_config("mysql"), logger)
    db.delete(QuesCollections, and_(QuesCollections.qid==qid, QuesCollections.uid==uid))


def to_cancel_collecta(aid, uid):
    parameter = UtilParameter()
    logger = UtilLogging(parameter, False, False, False)
    db = UtilMysql(parameter.get_config("mysql"), logger)
    db.delete(AnsCollections, and_(AnsCollections.aid==aid, AnsCollections.uid==uid))

