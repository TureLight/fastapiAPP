from typing import List
from pydantic import BaseModel


class CreateProjectModel(BaseModel):
    userName: str
    projectName: str
    testType: str
    testState: str
    testMaster: str = None
    tester: str = None
    devMaster: str = None
    submissionDate: str
    onlineDate: str


class CreateReportModel(BaseModel):
    userName: str
    projectName: str
    testState: str
    todayWork: str
    todayProblem: str = None
    urgentProblem: str = None


class UpdateReport(BaseModel):
    userName: str
    project_name: str
    test_state: str
    today_work: str
    today_problem: str = None
    urgent_problem: str = None
    id: str


class UpdateProjectModel(BaseModel):
    project_name: str
    test_type: str
    test_state: str
    test_master: str
    tester: str = None
    development_manager: str = None
    submission_time: str
    online_time: str
    id: str








