from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Integer, Text
from common.database import Base


class DTaskResultModule(Base):
    __tablename__ = 'task_result'
    id = Column(Integer, primary_key=True)
    task_name = Column(String)
    sys_name = Column(String)
    sys_module = Column(String)
    sys_api = Column(String)
    task_stat = Column(String)
    status = Column(String)
    response = Column(String)
    result = Column(Integer)
    timestamp = Column(Integer)
    create_time = Column(DateTime)
    operator = Column(String, unique=True)
    is_delete = Column(Integer)
