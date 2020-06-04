from typing import List
from pydantic import BaseModel


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








