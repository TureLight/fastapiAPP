from typing import List
from pydantic import BaseModel


class CreateProjectModel(BaseModel):
    id: int = None
    name: str
    tester: str
    virtualenv: str
    host: str
    com_header: str
    operator: str


class UpdateProjectModel(BaseModel):
    id: int = None
    name: str
    tester: str
    virtualenv: str
    host: str
    com_header: str
    operator: str


class CreateTestCaseSchema(BaseModel):
    case_set_id: int
    project_id: int = None
    case_id: int = None
    case_name: str = {'CAS': str}
    case_desc: str
    test_step: list
    # step_num: int
    # step_name: str
    # step_desc: str = None
    # up_set: int
    # tear_down: int
    # url: str
    # method: str
    # headers: str
    # params: str = None
    # form_data: str = None
    # json_data: str = None
    # need_assert: int
    # exp_statue: str
    # exp_extract: str
    operator: str












