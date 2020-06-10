from typing import List
from pydantic import BaseModel, Schema


class RunSystemTaskSchema(BaseModel):
    id: int
    name: str
    method: str
    variable: str
    headers: str
    params: str
    form_data: str
    status: int
    response: str
    operator: str
