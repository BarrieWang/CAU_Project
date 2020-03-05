import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy import exc
from sqlalchemy import and_, or_
# from util.util_logging import UtilLogging as ULog

Base = declarative_base()
# engine = None
# Session = None
# session = None


class Users(Base):
    """
    用户个人信息表
    """

    __tablename__ = 'user'
    uid = Column(String(20), primary_key=True)
    name = Column(String(50), nullable=False)
    passwd = Column(String(50), nullable=False)
    email = Column(String(50), unique=True)
    labelset = Column(String(300))
    regtime = Column(DateTime, default=datetime.datetime.now)  # 不能加括号，加了括号，以后永远是当前时间

    def __str__(self):
        return self.uid + " -- " + self.name + ":" + self.passwd + " -- " + str(self.regtime)


class Questions(Base):
    """
    问题数据表
    """

    __tablename__ = "question"
    qid = Column(String(20), primary_key=True)
    uid = Column(String(20), ForeignKey('user.uid'), nullable=False)
    label = Column(String(30))
    ques_content = Column(Text)
    ques_time = Column(DateTime, default=datetime.datetime.now)
    ques_collect = Column(Integer, default=0)


class Answers(Base):
    """
    回答数据表
    """

    __tablename__ = "answer"
    aid = Column(String(20), primary_key=True)
    uid = Column(String(20), ForeignKey('user.uid'), nullable=False)
    qid = Column(String(20), ForeignKey('question.qid'), nullable=False)
    ans_content = Column(LONGTEXT)
    ans_time = Column(DateTime, default=datetime.datetime.now)
    ans_collect = Column(Integer, default=0)


class QuesCollections(Base):
    """
    问题收藏信息表
    """

    __tablename__ = "ques_collection"
    cid = Column(String(20), primary_key=True)
    uid = Column(String(20), ForeignKey('user.uid'), nullable=False)
    qid = Column(String(20), ForeignKey('question.qid'), nullable=False)


class AnsCollections(Base):
    """
    回答收藏信息表
    """

    __tablename__ = "ans_collection"
    cid = Column(String(20), primary_key=True)
    uid = Column(String(20), ForeignKey('user.uid'), nullable=False)
    aid = Column(String(20), ForeignKey('answer.aid'), nullable=False)


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
            max_overflow=0,  # 超过连接池大小外最多创建的连接
            pool_size=10,  # 连接池大小
            pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
            pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）
        )
        # Base.metadata.create_all(self.engine)  # 建表
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def __del__(self):
        """
        断开连接
        """

        self.session.close()
        # Base.metadata.drop_all(self.engine)  # 删除表

    def insert(self, obj):
        """
        插入单条记录
        :param obj: 数据库记录对象
        :return:
        """

        try:
            self.session.add(obj)
            self.session.commit()
        except exc:
            self.logger.error("Wrong Insert Instruction")

    def insert_all(self, objs):
        """
        插入多条记录
        :param objs: 列表，中间的每个元素是一个要插入的记录对象
        :return:
        """

        try:
            self.session.add_all(objs)
            self.session.commit()
        except exc:
            self.logger.error("Wrong Insert Instruction")

    def delete(self, table, func=None):
        """
        删除指定条件的记录
        :param table: 数据所在表，输入对应的类名
        :param func: 筛选条件，输入表达式
            and_(x1,x2)表示同时满足，or_(y1,y2)表示任一条件满足, z.in_([])表示存在于列表中，~表示取反
        :return:
        """

        try:
            if func is not None:
                self.session.query(table).filter(func).delete()
            else:
                self.session.query(table).delete()
            self.session.commit()
        except exc:
            self.logger.error("Wrong Delete Instruction")

    def update(self, table, data, func=None):
        """
        修改指定条件的记录
        :param table: 数据所在表，输入对应的类名
        :param data: 需要修改的值，输入字典
        :param func: 筛选条件，输入表达式
        :return:
        """

        try:
            if func is not None:
                self.session.query(table).filter(func).update(data)
            else:
                self.session.query(table).update(data)
            self.session.commit()
        except exc:
            self.logger.error("Wrong Update Instruction")

    def select(self, table, func=None):
        """
        查询指定条件的记录
        :param table: 数据所在表，输入对应的类名
        :param func: 筛选条件，输入表达式
        :return:
        """

        result = []
        try:
            if func is not None:
                result = self.session.query(table).filter(func).all()
            else:
                result = self.session.query(table).all()
        except exc:
            self.logger.error("Wrong Update Instruction")
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
