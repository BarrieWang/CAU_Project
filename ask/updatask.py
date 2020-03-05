import sqlalchemy
from sqlalchemy.orm import sessionmaker
from util import util_mysql

#创建MySQL连接
db = sqlalchemy.create_engine('mysql://guest:Guestpass1!@47.93.56.66:3306/CAU_Project')

def query(uqid):
    '''
    查询函数
    :return:查询到的数据
    '''
    s = sessionmaker(bind=db)
    session = s()
    #条件查询
    res = session.query(util_mysql.Questions).filter_by(qid=uqid).all()
    print(res)
    return res

def updat(uqid, ulabel, ucontent):
    """
    更新函数
    :param uqid:问题ID, ulabel:问题类别, ucontent:问题内容
    :return: none
    """
    s = sessionmaker(bind=db)
    session = s()
    # 条件查询
    res = session.query(util_mysql.Questions).filter_by(qid=uqid).one()
    res.label = ulabel
    res.ques_content = ucontent
    session.commit()
    session.close()