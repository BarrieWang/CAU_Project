from util.util_mysql import Questions, Answers, QuesCollections, AnsCollections, and_


def delete(qaid, uid, db):
    """
    自动判别问题、回答并删除
    :param qaid:ID
    :param uid:用户ID
    :param db:数据库对象
    :return state:删除操作状态 AnsDel：回答删除成功 QuesDel：问题删除成功 Error：失败
    """
    if qaid[0] == 'A':
        return delet_ans(qaid, uid, db)
    elif qaid[0] == 'Q':
        return delet_ques(qaid, uid, db)
    else:
        return "Error"


def delet_ans(aid, uid, db):
    """
    删除回答及其收藏
    :param aid:问题ID
    :param uid:用户ID
    :param db:数据库对象
    :return state:删除操作状态
    """
    isOwner = db.select(Answers, and_(Answers.aid == aid, Answers.uid == uid))
    if len(isOwner) != 0:
        db.delete(AnsCollections, AnsCollections.aid == aid)
        db.delete(Answers, Answers.aid == aid)
        state = "AnsDel"
    else:
        state = "Error"
    return state


def delet_ques(qid, uid, db):
    """
    删除问题函数
    :param qid:问题ID
    :param uid:用户ID
    :param db:数据库对象
    :return: state:删除操作状态
    """
    isOwner = db.select(Questions, and_(Questions.qid == qid, Questions.uid == uid))
    if len(isOwner) != 0:
        flag = db.select(Answers.aid, Answers.qid == qid)
        flag = [item[0] for item in flag]
        db.delete(AnsCollections, and_(AnsCollections.aid == flag))
        db.delete(Answers, Answers.qid == qid)
        db.delete(QuesCollections, QuesCollections.qid == qid)
        db.delete(Questions, Questions.qid == qid)
        state = "QuesDel"
    else:
        state = "Error"
    return state
