from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Integer, Text
from common.database import Base


class DApiModule(Base):
    __tablename__ = 'sys_api'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    path = Column(String)
    method = Column(String)
    variable = Column(String)
    headers = Column(String)
    params = Column(String)
    form_data = Column(String)
    status = Column(Integer)
    response = Column(String)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
    operator = Column(String, unique=True)
    is_delete = Column(Integer)
    module_key = Column(Integer)


class DSystemModule(Base):
    __tablename__ = 'sys_name'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
    operator = Column(String, unique=True)
    is_delete = Column(Integer)


class DModuleModule(Base):
    __tablename__ = 'sys_module'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    host = Column(String)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
    operator = Column(String, unique=True)
    sys_key = Column(Integer)
    is_delete = Column(Integer)