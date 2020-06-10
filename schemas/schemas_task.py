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


class RunSystemTaskSchema(BaseModel):
    system_name: int
    module_name: int
    api_list: list
    run_data: PostDataForm
    operator: str
