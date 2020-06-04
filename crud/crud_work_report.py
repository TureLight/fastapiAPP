from sqlalchemy.orm import Session
from models.model_work import WorkReport, WorkProject
from sqlalchemy import func, or_
from datetime import datetime


def get_work_report(db: Session, page_num: int, page_size: int, query: str = None):
    now = (datetime.today()).strftime('%Y-%m-%d')
    project_obj = db.query(WorkProject.id, WorkProject.project_name).filter(WorkProject.is_delete == 0).all()
    if query or query != '':
        check_num = db.query(func.count(WorkReport.id)). \
            join(WorkProject, WorkProject.id == WorkReport.project_id). \
            filter(WorkProject.is_delete == 0, WorkReport.is_delete == 0, WorkReport.create_time == now,
                   or_(WorkProject.project_name.like('%{}%'.format(query)),
                       WorkProject.test_type.like('%{}%'.format(query)),
                       WorkProject.test_master.like('%{}%'.format(query)),
                       WorkProject.tester.like('%{}%'.format(query)),
                       WorkProject.development_manager.like('%{}%'.format(query)),
                       WorkProject.test_state.like('%{}%'.format(query)),)).scalar()
        result = db.query(WorkReport.id, WorkProject.project_name, WorkProject.test_type, WorkProject.test_master,
                          WorkProject.tester, WorkProject.development_manager, WorkProject.submission_time,
                          WorkProject.online_time, WorkProject.test_state, WorkReport.today_work,
                          WorkReport.today_problem, WorkReport.urgent_problem). \
            join(WorkReport, WorkProject.id == WorkReport.project_id). \
            filter(WorkProject.is_delete == 0, WorkReport.is_delete == 0, WorkReport.create_time == now,
                   or_(WorkProject.project_name.like('%{}%'.format(query)),
                       WorkProject.test_type.like('%{}%'.format(query)),
                       WorkProject.test_master.like('%{}%'.format(query)),
                       WorkProject.tester.like('%{}%'.format(query)),
                       WorkProject.development_manager.like('%{}%'.format(query)),
                       WorkProject.test_state.like('%{}%'.format(query)),)). \
            offset(int(page_size)*(int(page_num)-1)).limit(int(page_size)).all()
    else:
        check_num = db. \
            query(func.count(WorkReport.id)). \
            join(WorkProject, WorkReport.project_id == WorkProject.id).\
            filter(WorkReport.create_time == now, WorkProject.is_delete == 0, WorkReport.is_delete == 0).scalar()
        result = db. \
            query(WorkReport.id, WorkProject.project_name, WorkProject.test_type, WorkProject.test_master,
                  WorkProject.tester, WorkProject.development_manager, WorkProject.submission_time,
                  WorkProject.online_time, WorkProject.test_state, WorkReport.today_work,
                  WorkReport.today_problem, WorkReport.urgent_problem). \
            join(WorkReport, WorkProject.id == WorkReport.project_id). \
            filter(WorkReport.create_time == now, WorkProject.is_delete == 0, WorkReport.is_delete == 0). \
            offset(int(page_size)*(int(page_num)-1)).limit(int(page_size)).all()
    project_list = ({'id': item.id, 'project_name': item.project_name} for item in project_obj)
    report_list = ({'id': item.id, 'project_name': item.project_name, 'test_state': item.test_state,
                    'test_type': item.test_type, 'test_master': item.test_master, 'tester': item.tester,
                    'development_manager': item.development_manager, 'submission_time': item.submission_time,
                    'online_time': item.online_time, 'today_work': item.today_work,
                    'today_problem': item.today_problem, 'urgent_problem': item.urgent_problem
                    } for item in result
                   )
    list_dict = {'pageNum': page_num,
                 'total': check_num,
                 'workReportList': report_list,
                 'workProjectList': project_list
                 }
    return list_dict


def get_project(db: Session, page_num: int, page_size: int, query: str = None):
    off_set = int(page_size)*(int(page_num)-1)
    limit = int(page_size)
    # print(query)
    if query or query != '':
        check_num = db.query(func.count(WorkProject.id)). \
            filter(WorkProject.is_delete == 0,
                   or_(WorkProject.project_name.like('%{}%'.format(query)),
                       WorkProject.test_master.like('%{}%'.format(query)),
                       WorkProject.tester.like('%{}%'.format(query)),
                       WorkProject.development_manager.like('%{}%'.format(query))
                       )).scalar()
        result = db.query(WorkProject). \
            filter(WorkProject.is_delete == 0,
                   or_(WorkProject.project_name.like('%{}%'.format(query)),
                       WorkProject.test_master.like('%{}%'.format(query)),
                       WorkProject.tester.like('%{}%'.format(query)),
                       WorkProject.development_manager.like('%{}%'.format(query))
                       )
                   ). \
            order_by(WorkProject.create_time.desc()).offset(off_set).limit(limit).all()
    else:
        check_num = db.query(func.count(WorkProject.id)). \
            filter(WorkProject.is_delete == 0).scalar()
        result = db.query(WorkProject). \
            filter(WorkProject.is_delete == 0). \
            order_by(WorkProject.create_time.desc()).offset(off_set).limit(limit).all()

    list_dict = {'pageNum': page_num,
                 'total': check_num,
                 'workProjectList': [{'id': item.id, 'project_name': item.project_name, 'test_type': item.test_type,
                                      'test_state': item.test_state, 'test_master': item.test_master,
                                      'tester': item.tester, 'development_manager': item.development_manager,
                                      'submission_time': item.submission_time, 'online_time': item.online_time,
                                      'create_time': item.create_time
                                      } for item in result]
                 }
    return list_dict


def crud_get_under_project(db: Session, id):
    result = db.query(WorkReport.create_time, WorkProject.project_name, WorkProject.test_master, WorkProject.tester,
                      WorkReport.today_work, WorkReport.today_problem, WorkReport.urgent_problem). \
        join(WorkReport, WorkReport.project_id == WorkProject.id). \
        filter(WorkProject.id == id). \
        all()
    # print(result)
    return {'workReportList': [{'project_name': item.project_name, 'test_master': item.test_master,
                                'tester': item.tester, 'today_work': item.today_work,
                                'today_problem': item.today_problem, 'urgent_problem': item.urgent_problem,
                                'create_time': item.create_time} for item in result]}


def crud_get_edit_project(db: Session, id):
    result = db.query(WorkProject).filter(WorkProject.id == id).one_or_none()
    return result
