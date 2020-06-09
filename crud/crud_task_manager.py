from common.database import OperatorMysql
from models.model_interface import DApiModule, DModuleModule, DSystemModule, DTaskResultModule
from sqlalchemy.orm import Session
from celeryTask import tasks


def crud_get_task_page():
    conn = OperatorMysql()
    sql = "select sn.name sys_name, sm.name mod_name, sa.name api_name, sa.method, sa.variable, sa.headers," \
          "sa.params, sa.form_data " \
          "from " \
          "(sys_name sn left join sys_module sm on sn.id = sm.sys_key) " \
          "left join sys_api sa on sa.module_key=sm.id " \
          "where sn.is_delete=0 and sm.is_delete=0 and sa.is_delete=0 "
    res = conn.search(sql)
    return res


def crud_run_platform_task(task_name, username, url, params: tuple, start_date, end_date, one_day, page_size, operator, db: Session):
    tasks.platform_runner.delay(task_name, username, url, params, start_date, end_date, one_day, page_size, operator, db)


