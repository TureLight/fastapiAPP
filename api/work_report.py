from datetime import datetime, date
from fastapi import APIRouter, Depends
from models.model_work import WorkProject, WorkReport
from schemas.schemas_work import (CreateProjectModel,
                                  CreateReportModel,
                                  UpdateReport,
                                  UpdateProjectModel
                                  )
from crud.crud_user_control import user_menu_dict
from sqlalchemy.orm import Session
from crud.crud_work_report import (get_work_report,
                                   get_project,
                                   crud_get_under_project,
                                   crud_get_edit_project
                                   )
from common.database import get_db


router = APIRouter()


@router.get('/menu/')
async def get_menu(menu_dict: dict = Depends(user_menu_dict)):
    return menu_dict


@router.get('/workReport/')
async def today_work(userName: str, pageNum: int, pageSize: int, query: str = None, db: Session = Depends(get_db)):
    page_size = int(pageSize)
    page_num = int(pageNum)
    response = {'meta': {'status': 200, 'msg': '本日报告获取成功'}}
    try:
        list_dict = get_work_report(db, page_num=page_num, page_size=page_size, query=query)
        response['data'] = list_dict
        return response
    except Exception as e:
        return {'meta': {'status': 401, 'msg': '本日报告获取失败,错误信息{}'.format(e)}}


@router.post('/createProject/')
async def create_project(data: CreateProjectModel, db: Session = Depends(get_db)):
    response = {'meta': {'status': 201, 'msg': '新增项目成功'}}
    now = datetime.today()
    check_name = db.query(WorkProject.id).filter(WorkProject.project_name == data.projectName).one_or_none()
    if check_name is not None:
        return {'meta': {'status': 400, 'msg': '项目名称重复,请重新输入项目名称'}}
    try:
        db.add(WorkProject(project_name=data.projectName, test_state=data.testState, test_type=data.testType,
                           test_master=data.testMaster, tester=data.tester, development_manager=data.devMaster,
                           submission_time=data.submissionDate[:10], online_time=data.onlineDate[:10], create_time=now,
                           is_delete=0))
        db.commit()
        return response
    except Exception as e:
        return {'meta': {'status': 400, 'msg': '{}'.format(e)}}


@router.post('/createReport/')
async def create_report(data: CreateReportModel, db: Session = Depends(get_db)):
    response = {'meta': {'status': 201, 'msg': '新增项目成功'}}
    now = date.today()
    try:
        db.add(WorkReport(today_work=data.todayWork, today_problem=data.todayProblem, urgent_problem=data.urgentProblem,
                          create_time=now, is_delete=0, project_id=int(data.projectName.split(',')[0])))
        db.query(WorkProject).\
            filter(WorkProject.id == data.projectName.split(',')[0]).\
            update({'test_state': data.testState})
        db.commit()
        return response
    except Exception as e:
        return {'meta': {'status': 400, 'msg': '{}'.format(e)}}


@router.get('/get_edit_report/')
async def get_edit_report(id, db: Session = Depends(get_db)):
    try:
        result = db.query(WorkProject.project_name, WorkProject.test_type, WorkProject.test_state, WorkReport.id,
                          WorkReport.today_work, WorkReport.today_problem, WorkReport.urgent_problem).\
            join(WorkProject, WorkReport.project_id == WorkProject.id).\
            filter(WorkReport.id == int(id)).\
            one_or_none()
        if result:
            get_project_list = db.query(WorkProject.id, WorkProject.project_name).\
                filter(WorkProject.is_delete == 0).all()
            response = {'data': {'editWork': {'project_name': result.project_name, 'test_type': result.test_type,
                                              'test_state': result.test_state, 'id': result.id,
                                              'today_work': result.today_work, 'today_problem': result.today_problem,
                                              'urgent_problem': result.urgent_problem
                                              },
                                 'projectList': [{'id': item.id, 'project_name': item.project_name}
                                                 for item in get_project_list]
                                 },
                        'meta': {'status': 200, 'msg': '获取编辑内容成功!'}
                        }
            return response
        else:
            return {'meta': {'status': 400, 'msg': '获取编辑内容失败,请重新发起请求!'}}
    except Exception as e:
        return {'meta': {'status': 400, 'msg': '{}'.format(e)}}


@router.post('/update_report/')
async def update_report(data: UpdateReport, db: Session = Depends(get_db)):
    try:
        check = db.query(WorkProject.id).filter(WorkProject.project_name == data.project_name).one_or_none()
        db.query(WorkProject).\
            filter(WorkProject.id == check.id).\
            update({'test_state': data.test_state})
        db.query(WorkReport).\
            filter(WorkReport.id == data.id).\
            update({'today_work': data.today_work, 'today_problem': data.today_problem,
                    'urgent_problem': data.urgent_problem, 'project_id': check.id}
                   )
        db.commit()
        return {'meta': {'status': 200, 'msg': '更新日报成功'}}
    except Exception as e:
        return {'meta': {'status': 400, 'msg': '{}'.format(e)}}


@router.get('/delete_report/')
async def delete_report(id, db: Session = Depends(get_db)):
    try:
        db.query(WorkReport).filter(WorkReport.id == id).update({'is_delete': 1})
        db.commit()
        return {'meta': {'status': 200, 'msg': '删除日报成功'}}
    except Exception as e:
        return {'meta': {'status': 400, 'msg': '{}'.format(e)}}


@router.get('/show_project/')
async def show_project(userName, pageNum, pageSize, query: str = None, db: Session = Depends(get_db)):
    response = {'meta': {'status': 200, 'msg': '项目获取成功'}}
    # try:
    res = get_project(db=db, page_num=pageNum, page_size=pageSize, query=query)
    response['data'] = res
    return response
    # except Exception as e:
    #     return {'meta': {'status': 400, 'msg': '{}'.format(e)}}


@router.get('/show_under_project/')
async def get_report_under_project(id, db: Session = Depends(get_db)):
    response = {'meta': {'status': 200, 'msg': '项目获取成功'}}
    try:
        res = crud_get_under_project(db=db, id=id)
        response['data'] = res
        # print(response)
        return response

    except Exception as e:
        return {'meta': {'status': 400, 'msg': '{}'.format(e)}}


@router.get('/get_edit_project/')
async def edit_project(id, db: Session = Depends(get_db)):
    try:
        res = crud_get_edit_project(db=db, id=id)
        return {'data': {'edit_project': {'id': res.id, 'project_name': res.project_name, 'test_type': res.test_type,
                                          'test_state': res.test_state, 'test_master': res.test_master,
                                          'tester': res.tester, 'development_manager': res.development_manager,
                                          'submission_time': res.submission_time, 'online_time': res.online_time
                                          }
                         },
                'meta': {'status': 200, 'msg': '获取编辑内容成功'}
                }
    except Exception as e:
        return {'meta': {'status': 400, 'msg': '{}'.format(e)}}


@router.post('/update_project/')
async def update_project(data: UpdateProjectModel, db: Session = Depends(get_db)):
    try:
        check = db.query(WorkProject.id).\
            filter(WorkProject.project_name == data.project_name, WorkProject.id != data.id).\
            one_or_none()
        if check is None:
            db.query(WorkProject).\
                filter(WorkProject.id == data.id).\
                update({'project_name': data.project_name, 'test_type': data.test_type, 'test_state': data.test_state,
                        'test_master': data.test_master, 'tester': data.tester,
                        'development_manager': data.development_manager, 'submission_time': data.submission_time,
                        'online_time': data.online_time})
            db.commit()
            return {'meta': {'status': 200, 'msg': '更新项目成功'}}
        else:
            return {'meta': {'status': 400, 'msg': '项目名称重复,请重新输入'}}
    except Exception as e:
        return {'meta': {'status': 400, 'msg': '{}'.format(e)}}


@router.get('/delete_project/')
async def delete_project(id, db: Session = Depends(get_db)):
    try:
        db.query(WorkProject).filter(WorkProject.id == id).update({'is_delete': 1})
        db.commit()
        return {'meta': {'status': 200, 'msg': '删除项目成功'}}
    except Exception as e:
        return {'meta': {'status': 400, 'msg': '{}'.format(e)}}
