from util.util_mysql import UtilMysql, Questions, Answers
from util.util_logging import *
from util.util_parameter import *


def query(uuid, uqid, ulabel):
    '''
    查询函数
    :param:uuid:用户ID, uqid:问题ID, ulabel:问题标签
    :return:查询到全部数据
    '''
    parameter = UtilParameter()
    logger = UtilLogging(parameter, False, False, False)
    db = UtilMysql(parameter.get_config("mysql"), logger)
    if uuid is None and ulabel is None and uqid is None:
        res = db.select(Questions)
        return res
    elif uuid is not None:
        res = db.select(Questions, Questions.uid==uuid)
        return res
    elif ulabel is not None:
        res = db.select(Questions, Questions.label==ulabel)
        return res

