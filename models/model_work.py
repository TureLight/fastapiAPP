from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Boolean, Text
from common.database import Base


class WorkProject(Base):
    __tablename__ = 'work_project'

    id = Column(Integer, primary_key=True)
    project_name = Column(String, unique=True)
    test_type = Column(String)
    test_state = Column(String)
    test_master = Column(String)
    tester = Column(String)
    development_manager = Column(String)
    submission_time = Column(Date)
    online_time = Column(Date)
    create_time = Column(DateTime)
    is_delete = Column(Boolean)


class WorkReport(Base):
    __tablename__ = 'work_report'

    id = Column(Integer, primary_key=True)
    today_work = Column(Text)
    today_problem = Column(Text)
    urgent_problem = Column(Text)
    create_time = Column(Date)
    is_delete = Column(Boolean)
    project_id = Column(Integer, ForeignKey('work_project.id'))

