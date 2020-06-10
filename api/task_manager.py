from fastapi import APIRouter, Depends, BackgroundTasks
from common.database import get_db
from sqlalchemy.orm import Session
from crud.crud_task_manager import (crud_get_task_page,
                                    crud_get_task_by_sys,
                                    crud_run_platform_task,
                                    crud_get_task_by_sys_total, crud_get_module_by_sys
                                    )
from celeryTask.tasks import platform_runner
from crud.crud_interface_project import crud_query_case_set, crud_query_project
router = APIRouter()


@router.get('/task_page/')
def task_manage_page(db: Session = Depends(get_db)):
    res_sys = crud_get_task_page()
    res_pro = crud_query_project(db)
    res_set = crud_query_case_set()
    return {'data': {'system_list': res_sys,
                     'project_list': res_pro,
                     'set_list': res_set
                     },
            'meta': {'status': 200, 'msg': '获取成功！'}}


@router.get('/task_from_sys/')
def get_task_from_sys(query: int, page_num: int, page_size: int):
    res = crud_get_task_by_sys(query, page_num, page_size)
    # total = crud_get_task_by_sys_total(query)
    mod_list = crud_get_module_by_sys(query)
    return {'data': {'system_case_list': res,
                     'sys_module_list': mod_list,
                     # 'total': total[0]['count(sa.id)']
                     },
            'meta': {'status': 200, 'msg': '获取成功！'}}


@router.get('/run_task_from_sys/')
def run_task_from_sys(task_name, username, url, params: tuple, start_date, end_date,
                      one_day, page_size, operator, db: Session = Depends(get_db)):
    platform_runner()


def task_page(data, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    background_tasks.add_task(crud_run_platform_task())
    return {'meta': {'status': 202, 'msg': '任务已提交,后台已开始运行,稍后可前往任务管理页面查看运行进度'}}
