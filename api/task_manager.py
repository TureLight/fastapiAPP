from datetime import datetime, date
from fastapi import APIRouter, Depends, BackgroundTasks
from common.database import get_db
from sqlalchemy.orm import Session
from models.model_interface import ApiProject, CaseSet, ApiCase, ApiStep, TestData
from models.model_sys import SystemName
from crud.crud_task_manager import crud_get_task_page, crud_run_platform_task


def task_manage_page():
    res = crud_get_task_page()
    return res


def task_page(data, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    background_tasks.add_task(crud_run_platform_task())
    return {'meta': {'status': 202, 'msg': '任务已提交,后台已开始运行,稍后可前往任务管理页面查看运行进度'}}
