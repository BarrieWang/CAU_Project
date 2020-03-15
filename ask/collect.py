import uuid
from util.util_mysql import QuesCollections, AnsCollections, Questions, Answers, and_


def collect(qaid, uid, query, db):
    """
    自动判别问题、回答并收藏
    :param qaid:ID
    :param uid:用户ID
    :param query:是否仅查询
    :param db:数据库对象
    :return state:收藏操作状态 OK：成功 Duplicate：已收藏，重复操作 Not：未收藏 Error：失败
    """
    if qaid[0] == 'A':
        return to_collect_ans(uid, qaid, query, db)
    elif qaid[0] == 'Q':
        return to_collect_ques(uid, qaid, query, db)
    else:
        return "Error"


def cancel_collect(qaid, uid, db):
    """
    自动判别问题、回答并取消收藏
    :param qaid:ID
    :param uid:用户ID
    :param db:数据库对象
    :return state:收藏操作状态 OK：成功 Not：未收藏 Error：失败
    """
    if qaid[0] == 'A':
        return to_cancel_collecta(qaid, uid, db)
    elif qaid[0] == 'Q':
        return to_cancel_collectq(qaid, uid, db)
    else:
        return "Error"


def to_collect_ques(uid, qid, query, db):
    """
    收藏问题
    :param uid:用户ID
    :param qid: 问题ID
    :param query:是否仅查询
    :param db:数据库对象
    :return:
    """
    isCollected = db.select(QuesCollections, and_(QuesCollections.qid == qid, QuesCollections.uid == uid))
    # 判断是否已经收藏
    if len(isCollected) != 0:
        return "Duplicate"
    if query == "true":
        return "Not"
    else:
        cid = 'C' + uuid.uuid4().hex
        db.update(Questions, {Questions.ques_collect: Questions.ques_collect+1}, Questions.qid == qid)
        quesCollection = QuesCollections(cid=cid, uid=uid, qid=qid)
        db.insert(quesCollection)
        return "OK"


def to_collect_ans(uid, aid, query, db):
    """
    收藏回答
    :param uid:用户ID
    :param aid: 回答ID
    :param query:是否仅查询
    :param db:数据库对象
    :return:
    """
    isCollected = db.select(AnsCollections, and_(AnsCollections.aid == aid, AnsCollections.uid == uid))
    # 判断是否已经收藏
    if len(isCollected) != 0:
        return "Duplicate"
    if query == "true":
        return "Not"
    else:
        cid = 'C' + uuid.uuid4().hex
        db.update(Answers, {Answers.ans_collect: Answers.ans_collect + 1}, Answers.aid == aid)
        ansCollextion = AnsCollections(cid=cid, uid=uid, aid=aid)
        db.insert(ansCollextion)
        return "OK"


def to_cancel_collectq(qid, uid, db):
    isCollected = db.select(QuesCollections, and_(QuesCollections.qid == qid, QuesCollections.uid == uid))
    if len(isCollected) == 0:
        return "Not"
    db.delete(QuesCollections, and_(QuesCollections.qid == qid, QuesCollections.uid == uid))
    db.update(Questions, {Questions.ques_collect: Questions.ques_collect - 1}, Questions.qid == qid)
    return "OK"


def to_cancel_collecta(aid, uid, db):
    isCollected = db.select(AnsCollections, and_(AnsCollections.aid == aid, AnsCollections.uid == uid))
    if len(isCollected) == 0:
        return "Not"
    db.delete(AnsCollections, and_(AnsCollections.aid == aid, AnsCollections.uid == uid))
    db.update(Answers, {Answers.ans_collect: Answers.ans_collect - 1}, Answers.aid == aid)
    return "OK"
