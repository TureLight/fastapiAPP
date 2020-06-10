from sqlalchemy.orm import Session
from fastapi import Depends
from models.model_interface import ApiProject, CaseSet, ApiCase, ApiStep, TestData
from models.model_user import UserControl
from sqlalchemy import func, or_
from datetime import datetime
import requests
from common.database import OperatorMysql
import pymysql.cursors
import time
import re
from schemas.schemas_interface import (CreateProjectModel,
                                       UpdateProjectModel,
                                       CreateTestCaseSchema,
                                       TestStep,
                                       QuerySchema
                                       )


# 获取项目
def crud_get_project(db: Session, page_num: int, page_size: int, query: str = None):
    off_set = int(page_size)*(int(page_num)-1)
    limit = int(page_size)
    choice_list = db.query(UserControl.id, UserControl.name).filter(UserControl.is_active == 1).all()
    if query is None:
        num = db.query(func.count(ApiProject.id)).\
            filter(ApiProject.is_delete == 0).\
            scalar()
        result = db.query(ApiProject.id, ApiProject.name, ApiProject.tester, ApiProject.virtualenv, ApiProject.host,
                          ApiProject.com_header).\
            filter(ApiProject.is_delete == 0).\
            order_by(ApiProject.create_time.desc()).\
            offset(off_set).\
            limit(limit).\
            all()
    else:
        num = db.query(func.count(ApiProject.id)).\
            filter(ApiProject.is_delete == 0, ApiProject.name.like('%{}%'.format(query)))\
            .scalar()
        result = db.query(ApiProject.id, ApiProject.name, ApiProject.tester, ApiProject.virtualenv, ApiProject.host,
                          ApiProject.com_header). \
            filter(ApiProject.is_delete == 0, ApiProject.name.like('%{}%'.format(query))).\
            order_by(ApiProject.create_time.desc()).\
            offset(off_set).\
            limit(limit).\
            all()
    return {'total': num,
            'page_num': page_num,
            'project_list': [{"id": item.id, 'name': item.name, 'tester': item.tester,
                              'virtualenv': item.virtualenv, 'host': item.host, 'com_header': item.com_header
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


# 返回测试项目
def crud_query_project(db: Session):
    res1 = db.query(ApiProject.id, ApiProject.name, ApiProject.host).filter(ApiProject.is_delete == 0).all()
    res2 = [{'id': item.id, 'name': item.name, 'host': item.host} for item in res1]
    return res2


# 返回测试集合
def crud_query_case_set():
    conn = OperatorMysql()
    sql = "select id, name from case_set where is_delete=0 "
    res = conn.search(sql)
    return res


def crud_insert_step(db: Session, data: CreateTestCaseSchema):
    now = datetime.today()
    this_case_id = db.query(ApiCase.id).filter(ApiCase.name == data.test_case.case_name).one_or_none()
    all_obj = [ApiStep(step=item.step_num + 1, name="{}-{}".format(data.test_case.case_name, item.step_name),
                       desc=item.step_desc, set_up=item.set_up,
                       tear_down=item.tear_down, url=item.url, method=item.method, headers=item.headers,
                       params=item.params, form_data=item.form_data, json_data=item.json_data,
                       need_assert=item.need_assert, create_time=now, update_time=now, operator=data.operator,
                       variable=item.variable, is_delete=0, api_case_key=this_case_id.id)
               for item in data.test_step
               ]
    db.bulk_save_objects(all_obj)


def crud_insert_assert(db: Session, data: CreateTestCaseSchema):
    now = datetime.today()
    this_case_id = db.query(ApiCase.id).filter(ApiCase.name == data.test_case.case_name).one_or_none()
    this_id = db.query(ApiStep.id). \
        filter(ApiStep.api_case_key == this_case_id.id).order_by(ApiStep.step).all()
    for item, key in zip(data.test_step, this_id):
        print(item, key)
    assert_obj = db.add(TestData(assert_method=item.assert_method, exp_status=item.exp_status,
                                 exp_extract=item.exp_extract, create_time=now, update_time=now,
                                 operator=data.operator, is_delete=0, api_step_key=key[0])
                        for item, key in zip(data.test_step, this_id))
    db.bulk_save_objects(assert_obj)


def crud_create_case(db: Session, data: CreateTestCaseSchema):
    connection = pymysql.connect(host='localhost',
                                 port=3306,
                                 user='root',
                                 password='Fr39:.Gzj+WN',
                                 # password='123456',
                                 db='auto_test',
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)

    check_case_id = db.query(ApiCase.id).filter(ApiCase.name == data.test_case.case_name).one_or_none()
    if check_case_id is None:
        now = datetime.today()
        try:
            db.add(ApiCase(name=data.test_case.case_name, desc=data.test_case.case_desc,
                           create_time=now, update_time=now, operator=data.operator,
                           api_project_key=data.project_id, case_set_key=data.case_set_id, is_delete=0))
            db.commit()
            this_case_id = db.query(ApiCase.id).filter(ApiCase.name == data.test_case.case_name).one_or_none()
            insert_sql = "INSERT INTO `api_step` " \
                         "(`step`, `name`, `desc`, `set_up`, `tear_down`, `url`, `method`, `variable`, `headers`, " \
                         "`params`, `form_data`, `json_data`, `need_assert`, `create_time`, `update_time`, `operator`, " \
                         "`is_delete`, `api_case_key`) " \
                         "VALUES " \
                         "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            step_tuple = [(item.step_num+1, "{}-{}".format(data.test_case.case_name, item.step_name),
                           item.step_desc, item.set_up, item.tear_down, item.url, item.method, item.variable,
                           item.headers, item.params, item.form_data, item.json_data, item.need_assert,
                           now, now, data.operator, 0, this_case_id.id)
                          for item in data.test_step
                          ]
            with connection.cursor() as cursor:
                cursor.executemany(insert_sql, step_tuple)
                connection.commit()
                cursor.close()
            for item in data.test_step:
                with connection.cursor() as cursor:
                    id_sql = "select id from `api_step` where `name`=%s and `step`=%s"
                    value = ("{}-{}".format(data.test_case.case_name, item.step_name), item.step_num+1)
                    cursor.execute(id_sql, value)
                    res = cursor.fetchall()
                with connection.cursor() as cursor:
                    this_sql = "INSERT INTO `assert_data` (`assert_method`, `exp_status`, `exp_extract`, " \
                               "`create_time`, `update_time`, `operator`, `is_delete`, `api_step_key`) " \
                               "VALUES " \
                               "(%s, %s, %s, %s, %s, %s, %s, %s)"
                    values = (item.assert_method, item.exp_status, item.exp_extract, now, now, data.operator, 0, res[0]['id'])
                    cursor.execute(this_sql, values)
                    connection.commit()
                    cursor.close()
            connection.close()
            return {'meta': {'status': 200, 'msg': '添加用例成功！'}}
        except Exception as e:
            connection.close()
            return {'meta': {'status': 400, 'msg': '{}'.format(e)}}
    else:
        return {'meta': {'status': 400, 'msg': '用例名称重复！'}}


def crud_show_case_set(db: Session):
    # TODO: 测试集合编辑页面
    res1 = db.query(ApiProject.id, ApiProject.name).filter(ApiProject.is_delete == 0).all()
    res2 = db.query(CaseSet.id, CaseSet.name).filter(CaseSet.is_delete == 0).all()


def crud_assert(status, response, exp_status, exp_response):
    assert_code = True
    assert_response = True
    if str(status) != str(exp_status):
        assert_code = False
    if str(response).find(str(exp_response)) == -1:
        assert_response = False
    return {'code': assert_code, 'response': assert_response}


def crud_to_test_step(data: TestStep):
    try:
        url = "{}{}".format(data.host, data.url)
        # rules = re.compile(r'^{.*?}$')
        # if re.match(rules, data.headers) is None:
        headers = eval(data.headers)
        params = None
        f_data = None
        j_data = None
        res = None
        if data.params:
            params = eval(data.params)
        if data.form_data:
            f_data = eval(data.form_data)
        if data.json_data:
            j_data = eval(data.json_data)
        r_data = f_data if f_data is not None else j_data
        if data.method == 'GET':
            res = requests.get(url=url, headers=headers, params=params, data=r_data)
        elif data.method == 'POST':
            res = requests.post(url=url, headers=headers, params=params, data=r_data)
        elif data.method == 'PUT':
            res = requests.put(url=url, headers=headers, params=params, data=r_data)
        elif data.method == 'DELETE':
            res = requests.delete(url=url, headers=headers, params=params, data=r_data)
        res1 = crud_assert(res.status_code, res.content, data.exp_status, data.exp_extract)
        return {'code': res.status_code, 'response': res.text, 'assert': res1,
                'meta': {'status': 200, 'msg': '成功！'}}
    except Exception as e:
        return {'meta': {'status': 400, 'msg': '{}'.format(e)}}


def crud_return_project_case(query: int, page_num: int, page_size: int):
    conn = OperatorMysql()
    sql = "select " \
          "`a`.id case_id, `a`.name case_name, `a`.`desc` case_desc, `as`.step step_num , `as`.name step_name, " \
          " `as`.desc step_desc, `as`.set_up, `as`.tear_down, `as`.url, `as`.method, `as`.variable, `as`.headers, " \
          "`as`.params, `as`.form_data, `as`.json_data, `as`.need_assert, ad.assert_method, ad.exp_status, " \
          "ad.exp_extract " \
          "from " \
          "(api_case `a` left join api_step `as` on `a`.id = `as`.api_case_key) " \
          "left join assert_data `ad` on `as`.id=`ad`.api_step_key where a.is_delete=0 and `as`.is_delete=0 " \
          "and ad.is_delete=0 and a.api_project_key=%s order by a.id  limit %s, %s"
    res = conn.search(sql, (query, (page_num-1)*page_size, page_size))
    return res


def crud_return_project_case_total(query: int):
    conn = OperatorMysql()
    sql = "select " \
          "count(as.name) " \
          "from " \
          "(api_case `a` left join api_step `as` on `a`.id = `as`.api_case_key) " \
          "left join assert_data `ad` on `as`.id=`ad`.api_step_key where a.is_delete=0 and `as`.is_delete=0 " \
          "and ad.is_delete=0 and a.api_project_key=%s"
    res = conn.search(sql, (query,))
    return res


def crud_return_set_case(query: int, page_num: int, page_size: int):
    conn = OperatorMysql()
    sql = "select " \
          "`a`.id case_id, `a`.name case_name, `a`.`desc` case_desc, `as`.step step_num , `as`.name step_name, " \
          " `as`.desc step_desc, `as`.set_up, `as`.tear_down, `as`.url, `as`.method, `as`.variable, `as`.headers, " \
          "`as`.params, `as`.form_data, `as`.json_data, `as`.need_assert, ad.assert_method, ad.exp_status, " \
          "ad.exp_extract " \
          "from " \
          "(api_case `a` left join api_step `as` on `a`.id = `as`.api_case_key) " \
          "left join assert_data `ad` on `as`.id=`ad`.api_step_key where a.is_delete=0 and `as`.is_delete=0 " \
          "and ad.is_delete=0 and a.case_set_key=%s order by a.id  limit %s, %s"
    res = conn.search(sql, (query, (page_num-1)*page_size, page_size))
    return res


def crud_return_set_case_total(query: int):
    conn = OperatorMysql()
    sql = "select " \
          "count(as.name) " \
          "from " \
          "(api_case `a` left join api_step `as` on `a`.id = `as`.api_case_key) " \
          "left join assert_data `ad` on `as`.id=`ad`.api_step_key where a.is_delete=0 and `as`.is_delete=0 " \
          "and ad.is_delete=0 and a.case_set_key=%s"
    res = conn.search(sql, (query,))
    return res


if __name__ == '__main__':
    print(crud_return_project_case_total(4))
    print(len(crud_return_project_case(4,1,10)))