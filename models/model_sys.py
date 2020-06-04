from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Boolean, Text
from common.database import Base


class SystemName(Base):
    __tablename__ = 'sys_name'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
    operator = Column(String, unique=True)
    is_delete = Column(Boolean)


class SystemModule(Base):
    __tablename__ = 'sys_module'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
    operator = Column(String, unique=True)
    is_delete = Column(Boolean)
    sys_key = Column(Integer, ForeignKey('sys_name.id'))


class SystemApi(Base):
    __tablename__ = 'sys_api'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    method = Column(String)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
    operator = Column(String, unique=True)
    is_delete = Column(Boolean)
    module_key = Column(Integer, ForeignKey('sys_module.id'))