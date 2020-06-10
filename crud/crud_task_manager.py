from common.database import OperatorMysql
from models.model_sys import DApiModule, DModuleModule, DSystemModule
from models.model_task import DTaskResultModule
from sqlalchemy.orm import Session
from celeryTask import tasks


def crud_get_task_page():
    conn = OperatorMysql()
    sql = "select id, name from sys_name where is_delete=0"
    res = conn.search(sql)
    return res


def crud_get_task_by_sys(id: int, page_num: int, page_size: int):
    conn = OperatorMysql()
    sql = "select sa.id, sn.name sys_name, sn.host, sa.path, sm.name mod_name, sa.name api_name, " \
          "sa.method, sa.variable, sa.headers, sa.params, sa.form_data " \
          "from " \
          "(sys_name sn left join sys_module sm on sn.id = sm.sys_key) " \
          "left join sys_api sa on sa.module_key=sm.id " \
          "where sn.is_delete=0 and sm.is_delete=0 and sa.is_delete=0 and sn.id=%s order by sa.id"
    res = conn.search(sql, (id,))
    return res


def crud_get_module_by_sys(id: int):
    conn = OperatorMysql()
    sql2 = "select id, name from sys_module where is_delete=0 and sys_key=%s"
    mod_list = conn.search(sql2, (id,))
    return mod_list


def crud_get_task_by_sys_total(id: int):
    conn = OperatorMysql()
    sql = "select count(sa.id) " \
          "from " \
          "(sys_name sn left join sys_module sm on sn.id = sm.sys_key) " \
          "left join sys_api sa on sa.module_key=sm.id " \
          "where sn.is_delete=0 and sm.is_delete=0 and sa.is_delete=0 and sn.id=%s "
    res = conn.search(sql, (id,))
    return res


def crud_run_platform_task(task_name, username, url, params: tuple, start_date, end_date, one_day, page_size, operator, db: Session):
    tasks.platform_runner.delay(task_name, username, url, params, start_date, end_date, one_day, page_size, operator, db)


def crud_task_result_page():
    conn = OperatorMysql()
    sql = " select task_name, sys_name, sys_module, sys_api, task_stat, status, response, result, " \
          "create_time, operator " \
          "from task_result " \
          "where is_delete=0 " \
          "order by create_time desc limit 100 "
    res = conn.search(sql)
    sql1 = "select name from user_control where is_active=1"
    res2 = conn.search(sql1)
    return res, res2


def crud_search_result(date, user):
    conn = OperatorMysql()
    res = None
    if date is not None and user is not None:
        sql = " select task_name, sys_name, sys_module, sys_api, task_stat, status, response, result, " \
              "create_time, operator " \
          "from task_result " \
          "where is_delete=0 and create_time=%s and operator=%s " \
          "order by create_time desc"
        res = conn.search(sql, (date[0:10], user))
    elif date is not None and user is None:
        sql = " select task_name, sys_name, sys_module, sys_api, task_stat, status, response, result, " \
              "create_time, operator " \
          "from task_result " \
          "where is_delete=0 and create_time=%s " \
          "order by create_time desc"
        res = conn.search(sql, (date[0:10],))
    elif date is None and user is not None:
        sql = " select task_name, sys_name, sys_module, sys_api, task_stat, status, response, result, " \
              "create_time, operator " \
              "from task_result " \
              "where is_delete=0 and operator=%s " \
              "order by create_time desc"
        res = conn.search(sql, (user,))
    return res


if __name__ == "__main__":
    print(crud_get_task_by_sys_total(1))