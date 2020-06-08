from typing import List
from pydantic import BaseModel, Schema


class QuerySchema(BaseModel):
    query: int
    page_num: int
    page_size: int


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
    case_name: str
    case_desc: str = None


class StepSchema(BaseModel):
    step_num: int
    step_name: str
    step_desc: str = None
    set_up: int
    tear_down: int
    url: str
    method: str
    variable: str = None
    headers: str = None
    params: str = None
    form_data: str = None
    json_data: str = None
    need_assert: int
    assert_method: str = None
    exp_statue: str = None
    exp_extract: str = None


class AssertDataSchema(BaseModel):
    exp_statue: str
    exp_extract: str


class CreateTestCaseSchema(BaseModel):
    case_set_id: int = None
    project_id: int
    test_case: CaseSchema = None
    test_step: List[StepSchema] = None
    operator: str


class TestStep(BaseModel):
    exp_extract: str = None
    exp_statue: str = None
    form_data: str = None
    headers: str = None
    host: str
    json_data: str = None
    method: str
    need_assert: str
    params: str = None
    project_id: int
    set_up: str = None
    step_desc: str = None
    step_name: str = None
    step_num: int
    tear_down: str = None
    url: str
    variable: str = None












