from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql.cursors
import redis

# redis_pool = redis.ConnectionPool(host='', port=6379, password='')
# redis_info = redis.Redis(connection_pool=redis_pool)

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:Fr39:.Gzj+WN@localhost:3306/auto_test"
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/auto_test"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # echo=True,
    pool_pre_ping=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class OperatorMysql:

    def __init__(self):
        self.connection = pymysql.connect(host='localhost',
                                          port=3306,
                                          user='root',
                                          password='Fr39:.Gzj+WN',
                                          # password='123456',
                                          db='auto_test',
                                          charset='utf8',
                                          cursorclass=pymysql.cursors.DictCursor)

    def __del__(self):
        self.connection.close()

    def create_table(self, sql: str, params: tuple):
        """
        CREATE TABLE table_name (column_name column_type);
        :param sql: sql
        :param params: tuple value
        :return: bool and msg
        """
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            cursor.commit()
            cursor.close()

    def search(self, sql: str, params: tuple = None) -> list:
        """
        SELECT column_name,column_name
        FROM table_name
        [WHERE Clause]
        [LIMIT N][ OFFSET M]
        :param sql: sql
        :param params: tuple value
        :return: boll and  result
        """
        with self.connection.cursor() as cursor:
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
        return result

    def execute(self, sql: str, params: tuple or list):
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            self.connection.commit()
            cursor.close()

    def execute_many(self, sql: str, params: list):
        with self.connection.cursor() as cursor:
            cursor.executemany(sql, params)
            self.connection.commit()
            cursor.close()

    def insert(self, sql: str, params: tuple or list):
        """
        INSERT INTO table_name ( field1, field2,...fieldN )
                       VALUES
                       ( value1, value2,...valueN );
        :param sql: sql
        :param params: tuple value
        :return: boll and  msg
        """
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            self.connection.commit()
            cursor.close()

    def update(self, sql: str, params: tuple):
        """
        UPDATE table_name SET field1=new-value1, field2=new-value2
        [WHERE Clause]
        :param sql: sql
        :param params: tuple value
        :return: boll and  msg
        """
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            self.connection.commit()
            cursor.close()

    def delete(self, sql: str, params: tuple):
        """
        DELETE FROM table_name [WHERE Clause]
        :param sql: sql
        :param params: tuple value
        :return: boll and  msg
        """
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            self.connection.commit()
            cursor.close()


