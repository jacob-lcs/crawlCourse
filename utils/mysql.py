import MySQLdb
from config.server import server

# 获取服务器或本地配置信息
serverData = server()
ip = serverData["ip"]
password = serverData["password"]
port = serverData["port"]
database = serverData["database"]
user = serverData["user"]

db = MySQLdb.connect(ip, user, password, database, charset='utf8')


# 执行sql语句
def execute(sql):
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # 使用execute方法执行SQL语句
    cursor.execute(sql)

    db.commit()


# 关闭数据库连接
def close_db():
    db.close()
