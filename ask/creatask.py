import uuid
from util.util_mysql import UtilMysql, Questions
from util.util_logging import *
from util.util_parameter import *


def add(uid, label, ques_title, ques_content,):
    parameter = UtilParameter()
    logger = UtilLogging(parameter, False, False, False)
    db = UtilMysql(parameter.get_config("mysql"), logger)

    uqid = uuid.uuid4().hex
    uqid = 'Q' + uqid
    question = Questions(qid=uqid,uid=uid,label=label,ques_title=ques_title, ques_content=ques_content,ques_time=datetime.datetime.now(),ques_collect=0)
    db.insert(question)

