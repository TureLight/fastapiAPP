from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Integer, Text
from common.database import Base


class ApiProject(Base):
    __tablename__ = 'api_project'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    tester = Column(String)
    virtualenv = Column(String)
    host = Column(String)
    com_header = Column(String)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
    operator = Column(String, unique=True)
    is_delete = Column(Integer)


class CaseSet(Base):
    __tablename__ = 'case_set'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
    operator = Column(String, unique=True)
    is_delete = Column(Integer)


class ApiCase(Base):
    __tablename__ = 'api_case'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    desc = Column(String)
    times = Column(Integer)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
    operator = Column(String, unique=True)
    is_delete = Column(Integer)
    case_set_key = Column(Integer, ForeignKey('case_set.id'))
    api_project_key = Column(Integer, ForeignKey('api_project.id'))


class ApiStep(Base):
    __tablename__ = 'api_step'

    id = Column(Integer, primary_key=True)
    step = Column(Integer)
    name = Column(String, unique=True)
    desc = Column(String)
    set_up = Column(Integer)
    tear_down = Column(Integer)
    url = Column(String)
    method = Column(String)
    variable = Column(String)
    headers = Column(String)
    params = Column(String)
    form_data = Column(String)
    json_data = Column(String)
    need_assert = Column(Integer)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
    operator = Column(String, unique=True)
    is_delete = Column(Integer)
    api_case_key = Column(Integer, ForeignKey('api_case.id'))


class TestData(Base):
    __tablename__ = 'assert_data'

    id = Column(Integer, primary_key=True)
    assert_method = Column(String)
    statue = Column(String)
    extract = Column(String)
    exp_statue = Column(String)
    exp_extract = Column(String)
    result = Column(Integer)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
    operator = Column(String, unique=True)
    is_delete = Column(Integer)
    api_step_key = Column(Integer, ForeignKey('api_step.id'))