import sqlalchemy
from sqlalchemy.orm import sessionmaker
from util.util_mysql import Questions, Answers

# 创建MySQL连接
db = sqlalchemy.create_engine('mysql://guest:Guestpass1!@47.93.56.66:3306/CAU_Project')


def delet_ans(uqid):
    """
    删除问题的所有回答
    :return:
    :param:uqid:问题ID
    """
    ss = sessionmaker(bind=db)
    session = ss()
    session.query(Answers).filter_by(qid=uqid).delete()
    session.commit()
    session.close()


def delet_ques(uqid):
    """
    删除问题函数
    :param uqid:问题ID
    :return: none
    """
    s = sessionmaker(bind=db)
    session = s()
    delet_ans(uqid)
    res = session.query(Questions).get(uqid)
    session.delete(res)
    session.commit()
    session.close()


db.dispose()