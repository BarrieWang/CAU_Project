import uuid
from util.util_mysql import UtilMysql, QuesCollections, AnsCollections
from util.util_logging import *
from util.util_parameter import *


def to_collect_ques(uid, qid):
    parameter = UtilParameter()
    logger = UtilLogging(parameter, False, False, False)
    db = UtilMysql(parameter.get_config("mysql"), logger)
    cid = uuid.uuid4().hex
    quesCollextion = QuesCollections(cid=cid, uid=uid, qid=qid)
    db.insert(quesCollextion)


def to_collect_ans(uid, aid):
    parameter = UtilParameter()
    logger = UtilLogging(parameter, False, False, False)
    db = UtilMysql(parameter.get_config("mysql"), logger)
    cid = uuid.uuid4().hex
    ansCollextion = AnsCollections(cid=cid, uid=uid, aid=aid)
    db.insert(ansCollextion)