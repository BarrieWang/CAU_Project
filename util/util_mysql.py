import pymysql
# from util.util_logging import UtilLogging as ULog


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
                    self.cursor.execute("INSERT INTO %s VALUES (%s)" % d)
                    self.connect.commit()
                except pymysql.err:
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
                    self.cursor.execute("DELETE FROM %s WHERE %s = '%s'" % d)
                    self.connect.commit()
                except pymysql.err:
                    self. connect.rollback()  # Rollback in case there is any error
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
                    self.cursor.execute("UPDATE %s SET %s = '%s' WHERE %s = '%s'" % d)
                    self.connect.commit()
                except pymysql.err:
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
                self.cursor.execute("SELECT * FROM %s WHERE %s = '%s'" % d)
                result = self.cursor.fetchall()
            except pymysql.err:
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
