from typing import List
from pydantic import BaseModel


class CreateProjectModel(BaseModel):
    id: int = None
    name: str
    tester: str
    virtualenv: str
    host: str = None
    com_header: str = None
    operator: str


class UpdateProjectModel(BaseModel):
    id: int = None
    name: str
    tester: str
    virtualenv: str
    host: str = None
    com_header: str = None
    operator: str


class CaseSchema(BaseModel):
    id: int = None
    name: str
    desc: str = None


class StepSchema(BaseModel):
    step_num: int
    step_name: str
    step_desc: str = None
    set_up: int
    tear_down: int
    url: str
    method: str
    headers: str
    params: str = None
    form_data: str = None
    json_data: str = None
    need_assert: int


class AssertDataSchema(BaseModel):
    exp_statue: str
    exp_extract: str


class CreateTestCaseSchema(BaseModel):
    case_set_id: int = None
    project_id: int
    test_case: dict = CaseSchema
    api_step: list = [StepSchema]
    assert_data: list = [AssertDataSchema]
    operator: str












