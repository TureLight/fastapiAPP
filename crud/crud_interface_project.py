from sqlalchemy.orm import Session
from fastapi import Depends
from models.model_interface import ApiProject, CaseSet, ApiCase, ApiStep, TestData
from models.model_user import UserControl
from models.model_sys import SystemName
from sqlalchemy import func, or_
from datetime import datetime
from schemas.schemas_interface import CreateProjectModel, UpdateProjectModel


# 获取项目
def crud_get_project(db: Session, page_num: int, page_size: int, query: str = None):
    off_set = int(page_size)*(int(page_num)-1)
    limit = int(page_size)
    choice_list = db.query(UserControl.id, UserControl.name).filter(UserControl.is_active == 1).all()
    if query is None or query == '':
        num = db.query(func.count(ApiProject.id)).\
            filter(ApiProject.is_delete == 0).\
            scalar()
        result = db.query(ApiProject.id, ApiProject.name, ApiProject.tester, ApiProject.virtualenv, ApiProject.host).\
            filter(ApiProject.is_delete == 0).\
            order_by(ApiProject.create_time.desc()).\
            offset(off_set).\
            limit(limit).\
            all()
    else:
        num = db.query(func.count(ApiProject.id)).\
            filter(ApiProject.is_delete == 0, ApiProject.name.like('%{}%'.format(query)))\
            .scalar()
        result = db.query(ApiProject.id, ApiProject.name, ApiProject.tester, ApiProject.virtualenv, ApiProject.host). \
            filter(ApiProject.is_delete == 0, ApiProject.name.like('%{}%'.format(query))).\
            order_by(ApiProject.create_time.desc()).\
            offset(off_set).\
            limit(limit).\
            all()
    return {'total': num,
            'page_num': page_num,
            'project_list': [{"id": item.id, 'name': item.name, 'tester': item.tester,
                              'virtualenv': item.virtualenv, 'host': item.host
                              } for item in result
                             ],
            'choice_list': [{'id': item.id, 'name': item.name} for item in choice_list]
            }


def crud_detect_repetition_name_all(db: Session, data: CreateProjectModel):
    res = db.query(ApiProject.id).filter(ApiProject.name == data.name).one_or_none()
    if res is None:
        return True
    else:
        return False


# 创建项目
def crud_create_project(db: Session, data: CreateProjectModel, detect: bool = Depends(crud_detect_repetition_name_all)):
    now = datetime.today()
    if detect:
        db.add(ApiProject(name=data.name, tester=data.tester, virtualenv=data.virtualenv, host=data.host,
                          com_header=data.com_header, create_time=now, update_time=now, operator=data.operator,
                          is_delete=0
                          )
               )
        db.commit()
        return True
    else:
        return False


# 获取待编辑的项目
def crud_get_edit_project(db: Session, id: int):
    res = db.query(ApiProject.id, ApiProject.name, ApiProject.tester, ApiProject.virtualenv,
                   ApiProject.host, ApiProject.com_header).\
        filter(ApiProject.id == id).one_or_none()
    return {'get_edit_project': {'id': res.id, 'name': res.name, 'tester': res.tester, 'virtualenv': res.virtualenv,
                                 'host': res.host, 'com_header': res.com_header
                                 }
            }


def crud_detect_repetition_name(db: Session, data: UpdateProjectModel):
    res = db.query(ApiProject.id).\
        filter(ApiProject.name == data.name, ApiProject.id != data.id).\
        one_or_none()
    if res is None:
        return True
    else:
        return False


# 更新项目
def crud_update_project(db: Session, data: UpdateProjectModel, detect: bool = Depends(crud_detect_repetition_name)):
    now = datetime.today()
    if detect:
        db.query(ApiProject).\
            filter(ApiProject.id == data.id).\
            update({'name': data.name, 'virtualenv': data.virtualenv, 'tester': data.tester, 'host': data.host,
                    'com_header': data.com_header, 'update_time': now, 'operator': data.operator
                    }
                   )
        db.commit()
        return True
    else:
        return False


# 删除项目
def crud_delete_project(db: Session, id, operator):
    now = datetime.today()
    db.query(ApiProject).filter(ApiProject.id == id).update(
        {'update_time': now, 'operator': operator, 'is_delete': 1})
    db.commit()
