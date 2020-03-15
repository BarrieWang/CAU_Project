import uuid
from util.util_mysql import Questions


def add(uid, label, ques_title, ques_content, nameflag, db):
    uqid = uuid.uuid4().hex
    uqid = 'Q' + uqid
    if nameflag == 'true':
        noname = True
    else:
        noname = False
    question = Questions(qid=uqid, uid=uid, label=label, ques_title=ques_title,
                         ques_content=ques_content, ques_anonymous=noname)
    db.insert(question)
