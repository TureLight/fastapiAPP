from typing import List
from pydantic import BaseModel, Schema


class PostDataForm(BaseModel):
    task_name: str
    username: str
    password: str
    host: str
    start_date: str
    end_date: str
    one_day: str
    page_size: str


class ApiListSchema(BaseModel):
    sys_name: str
    host: str = None
    path: str = None
    mod_name: str
    api_name: str
    method: str
    variable: str = None
    headers: str = None
    params: str = None
    form_data: str = None


class RunSystemTaskSchema(BaseModel):
    system_name: int = None
    module_name: int = None
    api_list: List[ApiListSchema] = None
    run_data: PostDataForm = None
    operator: str
