import sqlalchemy
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from util import util_mysql

#创建连接
db = sqlalchemy.create_engine('mysql://guest:Guestpass1!@47.93.56.66:3306/CAU_Project')

def add(uuid,ulabel,uques_content):
    s = sessionmaker(bind=db)
    session = s()
    uqid = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    question = util_mysql.Questions(qid=uqid,uid=uuid,label=ulabel,ques_content=uques_content,ques_time=datetime.datetime.now(),ques_collect=0)
    session.add(question)
    session.commit()
    session.close()