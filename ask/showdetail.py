from util.util_mysql import Questions, Answers
import uuid


def to_show_details(uqid, db):
    """
    查询问题及其答案
    :param uqid: 问题ID
    :param db:数据库对象
    :return: 查询到的问题及其答案
    """
    ques = db.select(Questions, Questions.qid == uqid)[0]
    ans = db.select(Answers, Answers.qid == uqid)
    return ques, ans


def to_answer(uid, qid, acontent, nameflag, db):
    """
    建立回答
    :param uuid:回答用户ID
    :param uqid: 回答问题ID
    :param acontent: 回答内容
    :param db:数据库对象
    :return:
    """
    aid = 'A' + uuid.uuid4().hex
    if nameflag == 'true':
        noname = True
    else:
        noname = False
    answer = Answers(aid=aid, uid=uid, qid=qid, ans_content=acontent, ans_anonymous=noname)
    db.insert(answer)
