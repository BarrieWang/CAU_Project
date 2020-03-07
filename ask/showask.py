import sqlalchemy
from sqlalchemy.orm import sessionmaker
from util.util_mysql import Questions

#创建MySQL连接
db = sqlalchemy.create_engine('mysql://guest:Guestpass1!@47.93.56.66:3306/CAU_Project')

def query(uuid, uqid, ulabel):
    '''
    查询函数
    :param:uuid:用户ID, uqid:问题ID, ulabel:问题标签
    :return:查询到全部数据
    '''
    s = sessionmaker(bind=db)
    session = s()
    if uuid is None and ulabel is None and uqid is None:
        res = session.query(Questions).all()
        return res
    elif uuid is not None:
        res = session.query(Questions).filter_by(uid = uuid).all()
        return res
    elif ulabel is not None:
        res = session.query(Questions).filter_by(label = ulabel).all()
        return res

db.dispose()