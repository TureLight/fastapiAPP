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








