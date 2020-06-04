from typing import List
from pydantic import BaseModel


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

class CreateProjectModel(BaseModel):
    id: int
    name: str
    tester: str
    virtualenv: int
    host: str
    com_header: str
    operator: str
    sys_name: str


class UpdateProjectModel(BaseModel):
    id: int
    name: str
    tester: str
    virtualenv: int
    host: str
    com_header: str
    operator: str
    sys_name: str








