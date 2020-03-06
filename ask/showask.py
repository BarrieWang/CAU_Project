import sqlalchemy
from sqlalchemy.orm import sessionmaker
from util import util_mysql

#创建MySQL连接
db = sqlalchemy.create_engine('mysql://guest:Guestpass1!@47.93.56.66:3306/CAU_Project')

def query(uuid, ulabel):
    '''
    查询函数
    :param:uuid:用户ID,ulabel:问题标签
    :return:查询到全部数据
    '''
    s = sessionmaker(bind=db)
    session = s()
    if uuid is None and ulabel is None:
        res = session.query(util_mysql.Questions).all()
        #条件查询
        #res = session.query(util_mysql.Questions).filter()
        return res
    elif uuid is not None:
        res = session.query(util_mysql.Questions).filter_by(uid = uuid).all()
        return res
    elif ulabel is not None:
        res = session.query(util_mysql.Questions).filter_by(label = ulabel).all()
        return res

db.dispose()