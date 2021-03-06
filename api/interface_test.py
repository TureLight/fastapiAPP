from fastapi import APIRouter, Depends, BackgroundTasks
from common.database import get_db
from sqlalchemy.orm import Session
from schemas.schemas_interface import (CreateProjectModel,
                                       UpdateProjectModel,
                                       CreateTestCaseSchema,
                                       TestStep,
                                       QuerySchema
                                       )
from crud.crud_interface_project import (crud_get_project,
                                         crud_create_project,
                                         crud_get_edit_project,
                                         crud_update_project,
                                         crud_delete_project,
                                         crud_query_project,
                                         crud_create_case,
                                         crud_to_test_step,
                                         crud_return_project_case_total,
                                         crud_return_project_case,
                                         crud_query_case_set,
                                         crud_return_set_case,
                                         crud_return_set_case_total
                                         )

router = APIRouter()


@router.get('/get_interface_project/')
async def get_interface_project(page_num, page_size, query: str = None, db: Session = Depends(get_db)):
    try:
        result = crud_get_project(db=db, query=query, page_num=page_num, page_size=page_size)
        return {'data': result,
                'meta': {'status': 200, 'msg': '项目获取成功！'}}
    except Exception as e:
        return {'meta': {'status': 400, 'msg': '{}'.format(e)}}


@router.post('/create_interface_project/')
async def create_project(data: CreateProjectModel, db: Session = Depends(get_db)):
    try:
        res = crud_create_project(db=db, data=data)
        if res:
            return {'meta': {'status': 201, 'msg': '新增项目成功！'}}
        else:
            return {'meta': {'status': 401, 'msg': '项目名称重复，请重新输入！'}}
    except Exception as e:
        return {'meta': {'status': 400, 'msg': '{}'.format(e)}}


@router.get('/ready_to_edit_project/')
async def ready_edit_project(id, db: Session = Depends(get_db)):
    try:
        result = crud_get_edit_project(db=db, id=id)
        return {'data': result,
                'meta': {'status': 200, 'msg': '项目获取成功！'}
                }
    except Exception as e:
        return {'meta': {'status': 400, 'msg': '{}'.format(e)}}


@router.post('/update_project/')
async def update_project(data: UpdateProjectModel, db: Session = Depends(get_db)):
    try:
        result = crud_update_project(db=db, data=data)
        if result:
            return {'meta': {'status': 201, 'msg': '更新项目成功！'}}
        else:
            return {'meta': {'status': 401, 'msg': '项目名称重复，请重新输入！'}}
    except Exception as e:
        return {'meta': {'status': 400, 'msg': '{}'.format(e)}}


@router.get('/delete_project/')
async def delete_project(id, user, db: Session = Depends(get_db)):
    try:
        crud_delete_project(db=db, id=id, operator=user)
        return {'meta': {'status': 201, 'msg': '删除项目成功！'}}
    except Exception as e:
        return {'meta': {'status': 400, 'msg': '{}'.format(e)}}


@router.get('/ready_create_case/')
async def create_case_view(db: Session = Depends(get_db)):
    try:
        res = crud_query_project(db=db)
        return {'data': {'project_list': res},
                'meta': {'status': 200, 'msg': '成功！'}}
    except Exception as e:
        return {'meta': {'status': 400, 'msg': '{}'.format(e)}}


@router.post('/create_case/')
async def create_case(data: CreateTestCaseSchema, db: Session = Depends(get_db)):
    try:
        res = crud_create_case(db=db, data=data)
        return res
    except Exception as e:
        return {'meta': {'status': 400, 'msg': '{}'.format(e)}}


@router.post('/to_test_step/')
async def to_test_step(data: TestStep):
    try:
        res = crud_to_test_step(data=data)
        return res
    except Exception as e:
        return {'meta': {'status': 400, 'msg': '{}'.format(e)}}


@router.get('/create_edit_page/')
async def create_edit_case_page(db: Session = Depends(get_db)):
    try:
        res1 = crud_query_project(db)
        res2 = crud_query_case_set()
        return {'data': {'project_list': res1,
                         'set_list': res2
                         },
                'meta': {'status': 200, 'msg': '获取成功！'}
                }
    except Exception as e:
        return {'meta': {'status': 400, 'msg': '{}'.format(e)}}


@router.get('/query_project_case/')
async def query_project_case(query: int, page_num: int, page_size: int):
    try:
        res = crud_return_project_case(query, page_num, page_size)
        total = crud_return_project_case_total(query)
        return {'data': {'project_case_list': res, 'total': total[0]['count(as.name)']},
                'meta': {'status': 200, 'msg': '项目获取成功！'}
                }
    except Exception as e:
        return {'meta': {'status': 400, 'msg': '{}'.format(e)}}


@router.get('/query_set_case/')
async def query_set_case(query: int, page_num1: int, page_size1: int):
    try:
        res = crud_return_set_case(query, page_num1, page_size1)
        total = crud_return_set_case_total(query)
        return {'data': {'project_case_list': res, 'total': total[0]['count(as.name)']},
                'meta': {'status': 200, 'msg': '项目获取成功！'}
                }
    except Exception as e:
        return {'meta': {'status': 400, 'msg': '{}'.format(e)}}










