from typing import List
from pydantic import BaseModel


class CreateProjectModel(BaseModel):
    userName: str
    projectName: str
    testType: str
    testState: str
    testMaster: str
    tester: str
    devMaster: str
    submissionDate: str
    onlineDate: str


class CreateReportModel(BaseModel):
    userName: str
    projectName: str
    testState: str
    todayWork: str
    todayProblem: str
    urgentProblem: str


class UpdateReport(BaseModel):
    userName: str
    project_name: str
    test_state: str
    today_work: str
    today_problem: str
    urgent_problem: str
    id: str


class UpdateProjectModel(BaseModel):
    project_name: str
    test_type: str
    test_state: str
    test_master: str
    tester: str
    development_manager: str
    submission_time: str
    online_time: str
    id: str








