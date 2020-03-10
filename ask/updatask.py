from util.util_mysql import UtilMysql, Questions, Answers
from util.util_logging import *
from util.util_parameter import *


def query_content(uqid):
    '''
    查询问题内容函数
    :return:查询到的数据
    '''
    parameter = UtilParameter()
    logger = UtilLogging(parameter, False, False, False)
    db = UtilMysql(parameter.get_config("mysql"), logger)
    #条件查询
    res = db.select(Questions, Questions.qid==uqid)
    return res

def updat(uqid, ulabel, utitle, ucontent):
    """
    更新函数
    :param uqid:问题ID, ulabel:问题类别, ucontent:问题内容
    :return: none
    """
    parameter = UtilParameter()
    logger = UtilLogging(parameter, False, False, False)
    db = UtilMysql(parameter.get_config("mysql"), logger)
    db.update(Questions, {Questions.label:ulabel, Questions.ques_title:utitle, Questions.ques_content:ucontent}, Questions.qid==uqid)

