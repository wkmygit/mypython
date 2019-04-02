import pymssql

host = r"192.168.9.253\sql2008"
user = "sa"
pwd = "sgsa"
db = "HTERP_XIAN_2018"


class MSSQL:
    def __init__(self):  # 类的构造函数，初始化数据库连接ip或者域名，以及用户名，密码，要连接的数据库名称
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

    def __GetConnect(self):  # 得到数据库连接信息函数， 返回: conn.cursor()
        self.conn = pymssql.connect(
            host=self.host, user=self.user, password=self.pwd, database=self.db, charset='utf8')
        cur = self.conn.cursor()  # 将数据库连接信息，赋值给cur。
        if not cur:
            return(NameError, "连接数据库失败")
        else:
            return cur

    # 执行查询语句,返回的是一个包含tuple的list，list的元素是记录行，tuple的元素是每行记录的字段
    def exec_query(self, sql):  # 执行Sql语句函数，返回结果
        cur = self.__GetConnect()  # 获得数据库连接信息
        cur.execute(sql)  # 执行Sql语句
        resList = cur.fetchall()  # 获得所有的查询结果
        # 查询完毕后必须关闭连接
        self.conn.close()  # 返回查询结果
        return resList

    # 执行SQL语句,返回影响行数
    def exec_query_row(self, sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()
        return cur.rowcount

    # 批量写入数据,返回影响行数
    def exec_batch_insert(self, sql, data):
        cur = self.__GetConnect()
        cur.executemany(sql, data)
        self.conn.commit()
        self.conn.close()
        return cur.rowcount
