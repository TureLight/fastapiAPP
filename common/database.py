from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import redis

# redis_pool = redis.ConnectionPool(host='', port=6379, password='')
# redis_info = redis.Redis(connection_pool=redis_pool)

# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:Fr39:.Gzj+WN@localhost:3306/auto_test"
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:zhangxin123456@localhost:3306/auto_test"
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

