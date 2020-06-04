from datetime import datetime, date
from fastapi import APIRouter, Depends
from common.database import get_db
from sqlalchemy.orm import Session
from models.model_interface import ApiProject, CaseSet, ApiCase, ApiStep, TestData
from models.model_sys import SystemName
from schemas.schemas_interface import (CreateProjectModel,
                                       UpdateProjectModel,
                                       )
from crud.crud_interface_project import (crud_get_project,
                                         crud_create_project,
                                         crud_get_edit_project,
                                         crud_update_project,
                                         crud_delete_project
                                         )

router = APIRouter()


@router.get('/get_interface_project/')
async def get_interface_project(query, page_num, page_size, db: Session = Depends(get_db)):
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
def delete_project(id, user, db: Session = Depends(get_db)):
    try:
        crud_delete_project(db=db, id=id, operator=user)
        return {'meta': {'status': 201, 'msg': '删除项目成功！'}}
    except Exception as e:
        return {'meta': {'status': 400, 'msg': '{}'.format(e)}}




