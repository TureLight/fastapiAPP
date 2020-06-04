from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Boolean, Text
from common.database import Base


class UserControl(Base):
    __tablename__ = 'user_control'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    name = Column(String)
    is_active = Column(Boolean)
    create_time = Column(DateTime)


class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    api_case_id = Column(String)
    api_step_id = Column(String)
    case_set_id = Column(String)
    api_project_id = Column(String)
    task_name = Column(String)
    timer = Column(DateTime)
    task_type = Column(Integer)
    status = Column(Integer)
    run_time = Column(Integer)
    result = Column(String)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
