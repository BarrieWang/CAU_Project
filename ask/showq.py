from util.util_mysql import Questions, Answers, QuesCollections, AnsCollections


def query(uuid, uqid, ulabel, db):
    '''
    查询函数
    :param uuid:用户ID
    :param uqid:问题ID
    :param ulabel:问题标签
    :param db:数据库对象
    :return:查询到全部数据
    '''
    if uuid is None and ulabel is None and uqid is None:
        res = db.select(Questions)
        return res
    elif uuid is not None:
        res = db.select(Questions, Questions.uid == uuid)
        return res
    elif ulabel is not None:
        res = db.select(Questions, Questions.label == ulabel)
        return res


def queryA(uid, db):
    ans = db.select(Answers, Answers.uid == uid)
    for an in ans:
        an.ques_title = db.select(Questions, Questions.qid == an.qid)[0].ques_title
    return ans


def queryCQ(uid, db):
    """
    查询用户收藏问题
    :param uid: 用户ID
    :param db:数据库对象
    :return: 问题对象列表
    """
    tem = db.select(QuesCollections.qid, QuesCollections.uid == uid)
    tem = [item[0] for item in tem]
    ques = db.select(Questions, Questions.qid.in_(tem))
    return ques


def queryCA(uid, db):
    """
    查询用户收藏答案
    :param uid: 用户ID
    :param db:数据库对象
    :return: 回答对象列表
    """
    tem = db.select(AnsCollections.aid, AnsCollections.uid == uid)
    tem = [item[0] for item in tem]
    ans = db.select(Answers, Answers.aid.in_(tem))
    for an in ans:
        an.ques_title = db.select(Questions, Questions.qid == an.qid)[0].ques_title
    return ans
