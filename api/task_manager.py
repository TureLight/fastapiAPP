from fastapi import APIRouter, Depends, BackgroundTasks
from common.database import get_db
from sqlalchemy.orm import Session
from crud.crud_task_manager import (crud_get_task_page,
                                    crud_get_task_by_sys,
                                    crud_run_platform_task,
                                    crud_get_task_by_sys_total,
                                    crud_get_module_by_sys,
                                    crud_task_result_page,
                                    crud_search_result
                                    )
from celeryTask.tasks import platform_runner
from crud.crud_interface_project import crud_query_case_set, crud_query_project
from schemas.schemas_task import RunSystemTaskSchema
import time

router = APIRouter()


@router.get('/task_page/')
async def task_manage_page(db: Session = Depends(get_db)):
    try:
        res_sys = crud_get_task_page()
        res_pro = crud_query_project(db)
        res_set = crud_query_case_set()
        return {'data': {'system_list': res_sys,
                         'project_list': res_pro,
                         'set_list': res_set
                         },
                'meta': {'status': 200, 'msg': '获取成功！'}}
    except Exception as e:
        return {'meta': {'status': 400, 'msg': '{}'.format(e)}}


@router.get('/task_from_sys/')
async def get_task_from_sys(query: int, page_num: int, page_size: int):
    try:
        res = crud_get_task_by_sys(query, page_num, page_size)
        # total = crud_get_task_by_sys_total(query)
        mod_list = crud_get_module_by_sys(query)
        return {'data': {'system_case_list': res,
                         'sys_module_list': mod_list,
                         # 'total': total[0]['count(sa.id)']
                         },
                'meta': {'status': 200, 'msg': '获取成功！'}}
    except Exception as e:
        return {'meta': {'status': 400, 'msg': '{}'.format(e)}}


@router.post('/run_task_from_sys/')
async def run_task_from_sys(data: RunSystemTaskSchema, background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(platform_runner, data)
        return {'meta': {'status': 202, 'msg': '任务已提交,后台已开始运行,稍后可前往任务管理页面查看运行进度'}}
    except Exception as e:
        return {'meta': {'status': 400, 'msg': '{}'.format(e)}}


@router.get('/get_result_page/')
async def get_task_result_page():
    try:
        res1, res2 = crud_task_result_page()
        return {'data': {'task_result_list': res1, 'tester_list': res2},
                'meta': {'status': 200, 'msg': '获取成功！'}}
    except Exception as e:
        return {'meta': {'status': 400, 'msg': '{}'.format(e)}}


@router.get('/search_result/')
async def get_search_result(choice_date=None, choice_tester=None):
    try:
        if choice_date is None and choice_tester is None:
            return {'meta': {'status': 400, 'msg': '查询参数违法!'}}
        else:
            res = crud_search_result(choice_date, choice_tester)
            return {'data': {'task_result_list': res},
                    'meta': {'status': 200, 'msg': '获取成功！'}}
    except Exception as e:
        return {'meta': {'status': 400, 'msg': '{}'.format(e)}}


# def task_page(data, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
#     background_tasks.add_task(crud_run_platform_task())
#     return {'meta': {'status': 202, 'msg': '任务已提交,后台已开始运行,稍后可前往任务管理页面查看运行进度'}}



