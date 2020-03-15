# coding=utf-8
import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy import exc
from sqlalchemy import and_, or_
from flask_login import UserMixin
from flask_login._compat import text_type
# from util.util_logging import UtilLogging as ULog

Base = declarative_base()
# engine = None
# Session = None
# session = None
labels = ["xuexi", "huodong", "xunwu", "chushou", "qiugou", "huzhu", "zhaopin"]
# "学习交流", "活动通知", "寻物招领", "二手出售", "二手求购", "互助问答", "招聘求职"


class Users(UserMixin, Base):
    """
    用户个人信息表
    """

    __tablename__ = 'user'
    uid = Column(String(40), primary_key=True)
    name = Column(String(50), nullable=False)
    passwd = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    labelset = Column(String(300), default="")  # 用户偏好，若干个用逗号连接的label字符串
    regtime = Column(DateTime, default=datetime.datetime.now)  # 不能加括号，加了括号，以后永远是当前时间
    authoriation = Column(String(5), default='1', nullable=False)

    def __str__(self):
        return self.uid + " -- " + self.name + " : " + self.passwd + " -- " + str(self.regtime)

    def get_id(self):
        return text_type(self.uid)


class UserCounts(Base):
    """
    用户创作信息统计表
    """

    __tablename__ = "user_count"
    uid = Column(String(40), primary_key=True)
    list = ["0" for _ in labels]
    total_count = Column(String(100), default=",".join(list))  # 整体创作量，对应每个label，用逗号隔开
    recent_count = Column(String(100), default=",".join(list))  # 近期创作量，对应每个label，用逗号隔开
    recent_qid = Column(LONGTEXT, default="")  # 近期创作的问题，若干个用逗号连接的qid字符串
    total_count_2 = Column(String(100), default=",".join(list))  # 整体浏览量
    recent_count_2 = Column(String(100), default=",".join(list))  # 近期浏览量
    recent_qid_2 = Column(LONGTEXT, default="")  # 近期浏览的问题

    def __str__(self):
        return self.uid + " -- " + self.total_count + " / " + self.recent_count\
               + "\n" + self.recent_qid


class Questions(Base):
    """
    问题数据表
    """

    __tablename__ = "question"
    qid = Column(String(40), primary_key=True)
    uid = Column(String(40), ForeignKey('user.uid'), nullable=False)
    label = Column(String(30))
    ques_title = Column(String(50))
    ques_content = Column(Text)
    ques_time = Column(DateTime, default=datetime.datetime.now)
    ques_collect = Column(Integer, default=0)
    ques_anonymous = Column(Boolean, default=False)
    uname = None
    uavatar = None

    def __str__(self):
        return self.qid + " -- " + self.uid\
               + "\n" + self.label + " -- " + self.ques_title + " : " + self.ques_content \
               + "\n" + str(self.ques_time) + " -- " + str(self.ques_collect)


class Answers(Base):
    """
    回答数据表
    """

    __tablename__ = "answer"
    aid = Column(String(40), primary_key=True)
    uid = Column(String(40), ForeignKey('user.uid'), nullable=False)
    qid = Column(String(40), ForeignKey('question.qid'), nullable=False)
    ans_content = Column(LONGTEXT)
    ans_time = Column(DateTime, default=datetime.datetime.now)
    ans_collect = Column(Integer, default=0)
    ans_anonymous = Column(Boolean, default=False)
    uname = None
    uavatar = None
    ques_title = None

    def __str__(self):
        return self.aid + " -- " + self.uid + " / " + self.qid\
               + "\n" + self.ans_content \
               + "\n" + str(self.ans_time) + " -- " + str(self.ans_collect)


class QuesCollections(Base):
    """
    问题收藏信息表
    """

    __tablename__ = "ques_collection"
    cid = Column(String(40), primary_key=True)
    uid = Column(String(40), ForeignKey('user.uid'), nullable=False)
    qid = Column(String(40), ForeignKey('question.qid'), nullable=False)

    def __str__(self):
        return self.cid + " -- " + self.uid + " / " + self.qid


class AnsCollections(Base):
    """
    回答收藏信息表
    """

    __tablename__ = "ans_collection"
    cid = Column(String(40), primary_key=True)
    uid = Column(String(40), ForeignKey('user.uid'), nullable=False)
    aid = Column(String(40), ForeignKey('answer.aid'), nullable=False)

    def __str__(self):
        return self.cid + " -- " + self.uid + " / " + self.aid


def get_conn_url(args):
    """
    获取参数，完成数据库连接的地址
    """

    host = args["host"]
    port = args["port"]
    user = args["user"]
    passwd = args["passwd"]
    database = args["database"]
    url = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4".format(user, passwd, host, str(port), database)
    # print(url)
    return url


class UtilMysql:

    def __init__(self, args, logger):
        """
        完成对数据库的连接
        """

        self.logger = logger
        self.engine = create_engine(
            get_conn_url(args),
            encoding="utf-8",
            max_overflow=0,  # 超过连接池大小外最多创建的连接
            pool_size=10,  # 连接池大小
            pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
            pool_recycle=-1,  # 多久之后对线程池中的线程进行一次连接的回收（重置）
        )
        # Base.metadata.create_all(self.engine)  # 建表
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def __del__(self):
        """
        断开连接
        """

        self.session.close()
        self.Session.close_all()
        # Base.metadata.drop_all(self.engine)  # 删除表
        self.engine.dispose()

    def display(self, table=None):
        """
        查看表中全部记录
        :param table: 数据所在表，输入对应的类名
        :return:
        """

        if table is not None:
            for rec in self.select(table):
                print(rec)
        else:
            for table_ in [Users, UserCounts, Questions, Answers, QuesCollections, AnsCollections]:
                for rec in self.select(table_):
                    print(rec)
                print()

    def get_ques(self, qids):
        """
        根据所给qid列表，获取对应的Question对象
        """

        return self.select(Questions, Questions.qid.in_(qids))

    def insert(self, obj):
        """
        插入单条记录
        :param obj: 数据库记录对象
        :return:
        """

        # session = self.Session()
        try:
            self.session.add(obj)
            self.session.commit()
        except exc.SQLAlchemyError:
            self.logger.error("Wrong Insert Instruction")
        # session.close()

    def insert_all(self, objs):
        """
        插入多条记录
        :param objs: 列表，中间的每个元素是一个要插入的记录对象
        :return:
        """

        # session = self.Session()
        try:
            self.session.add_all(objs)
            self.session.commit()
        except exc.SQLAlchemyError:
            self.logger.error("Wrong Insert Instruction")
        # session.close()

    def delete(self, table, func=None):
        """
        删除指定条件的记录
        :param table: 数据所在表，输入对应的类名
        :param func: 筛选条件，输入表达式
            and_(x1,x2)表示同时满足，or_(y1,y2)表示任一条件满足, z.in_([])表示存在于列表中，~表示取反
        :return:
        """

        # session = self.Session()
        try:
            if func is not None:
                self.session.query(table).filter(func).delete()
            else:
                self.session.query(table).delete()
            self.session.commit()
        except exc.SQLAlchemyError:
            self.logger.error("Wrong Delete Instruction")
        # session.close()

    def update(self, table, data, func=None):
        """
        修改指定条件的记录
        :param table: 数据所在表，输入对应的类名
        :param data: 需要修改的值，输入字典
        :param func: 筛选条件，输入表达式
        :return:
        """

        # session = self.Session()
        try:
            if func is not None:
                self.session.query(table).filter(func).update(data)
            else:
                self.session.query(table).update(data)
            self.session.commit()
        except exc.SQLAlchemyError:
            self.logger.error("Wrong Update Instruction")
        # session.close()

    def select(self, table, func=None):
        """
        查询指定条件的记录
        :param table: 数据所在表，输入对应的类名
        :param func: 筛选条件，输入表达式
        :return:
        """

        result = []
        # session = self.Session()
        try:
            if func is not None:
                result = self.session.query(table).filter(func).all()
            else:
                result = self.session.query(table).all()
        except exc.SQLAlchemyError:
            self.logger.error("Wrong Select Instruction")
        # session.close()
        return result


'''
import pymysql


class UtilMysql:
    """
    连接数据库并完成数据库操作
    """

    def __init__(self, args, logger):
        """
        构造函数，完成对数据库的连接
        """

        host = args["host"]
        port = args["port"]
        user = args["user"]
        passwd = args["passwd"]
        database = args["database"]

        self.connect = pymysql.connect(
            host=host, port=port, user=user, passwd=passwd, database=database,
            db="python", charset='utf8'
        )
        self.cursor = self.connect.cursor()
        self.logger = logger

    def __del__(self):
        """
        析构函数，断开连接
        """
        self.cursor.close()
        self.connect.close()

    def insert_mysql(self, data=None, sqls=None):
        """
        根据指定参数链接数据库，并完成插入操作，允许多条指令
        :param data: 需要插入的数据，list of cuples，cuple为表名和数据
            INSERT INTO %s VALUES (%s)
        :param sqls: 需要执行的插入指令
        :return:
        """

        if data is not None:
            for d in data:
                try:
                    self.cursor.execute("INSERT INTO %s VALUES (%s);" % d)
                    self.connect.commit()
                except pymysql.err.ProgrammingError:
                    self.connect.rollback()  # Rollback in case there is any error
                    self.logger.error("Wrong Insert Instruction")
        if sqls is not None:
            for sql in sqls:
                try:
                    self.cursor.execute(sql)
                    self.connect.commit()
                except pymysql.err:
                    self.connect.rollback()  # Rollback in case there is any error
                    self.logger.error("Wrong Insert Instruction")

    def delete_mysql(self, data=None, sqls=None):
        """
        根据指定参数链接数据库，并完成删除操作，允许多条指令
        :param data: 需要删除的数据，list of cuples，cuple为表名、主键名、主键值
            DELETE FROM %s WHERE %s = '%s'
        :param sqls: 需要执行的删除指令
        :return:
        """

        if data is not None:
            for d in data:
                try:
                    self.cursor.execute("DELETE FROM %s WHERE %s = '%s';" % d)
                    self.connect.commit()
                except pymysql.err.ProgrammingError:
                    self.connect.rollback()  # Rollback in case there is any error
                    self.logger.error("Wrong Delete Instruction")
        if sqls is not None:
            for sql in sqls:
                try:
                    self.cursor.execute(sql)
                    self.connect.commit()
                except pymysql.err:
                    self.connect.rollback()  # Rollback in case there is any error
                    self.logger.error("Wrong Delete Instruction")

    def update_mysql(self, data=None, sqls=None):
        """
        根据指定参数链接数据库，并完成修改操作，允许多条指令
        :param data: 需要修改的数据，list of cuples，cuple为表名、属性名、属性值、主键名、主键值
            UPDATE %s SET %s = '%s' WHERE %s = '%s'
        :param sqls: 需要执行的修改指令
        :return:
        """

        if data is not None:
            for d in data:
                try:
                    self.cursor.execute("UPDATE %s SET %s = '%s' WHERE %s = '%s';" % d)
                    self.connect.commit()
                except pymysql.err.ProgrammingError:
                    self.connect.rollback()  # Rollback in case there is any error
                    self.logger.error("Wrong Update Instruction")
        if sqls is not None:
            for sql in sqls:
                try:
                    self.cursor.execute(sql)
                    self.connect.commit()
                except pymysql.err:
                    self.connect.rollback()  # Rollback in case there is any error
                    self.logger.error("Wrong Update Instruction")

    def select_mysql(self, d=None, sql=None):
        """
        根据指定参数链接数据库，并完成查询操作，允许单条指令
        :param d: 需要查询的条件，cuple，为表名、属性名、属性值
            SELECT * FROM %s WHERE %s = '%s'
        :param sql: 需要执行的查询指令
        :return: 查询结果，list of cuples，需要对单个cuple进行整理，如直接list(cuple)
        """

        result = []
        if d is not None:
            try:
                self.cursor.execute("SELECT * FROM %s WHERE %s = '%s';" % d)
                result = self.cursor.fetchall()
            except pymysql.err.ProgrammingError:
                self.connect.rollback()  # Rollback in case there is any error
                self.logger.error("Wrong Select Instruction")
        if sql is not None:
            try:
                self.cursor.execute(sql)
                result = self.cursor.fetchall()
            except pymysql.err:
                self.connect.rollback()  # Rollback in case there is any error
                self.logger.error("Wrong Select Instruction")
        return result
'''
