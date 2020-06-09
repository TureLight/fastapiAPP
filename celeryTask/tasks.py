from celery import Celery
from common.database import OperatorMysql
from models.model_interface import DApiModule, DModuleModule, DSystemModule, DTaskResultModule
from sqlalchemy.orm import Session
import json
import requests
import uuid
import datetime
import re

app = Celery()
app.config_from_object("celeryConfig")


def platform_login(username, url):
    today = datetime.datetime.today()
    msg_id = str(uuid.uuid4()).replace('-', '')
    log_id = str(uuid.uuid4()).replace('-', '')
    trns_id = str(uuid.uuid4()).replace('-', '')
    login_data = {"header": {"version": 1,
                             "send_sysname": "jgcp",
                             "recv_sysname": "",
                             "sender": "jgcp",
                             "receiver": "",
                             "channel": "MS",
                             "msg_type": "DL.001",
                             "msg_id": "".format(msg_id),
                             "log_id": "".format(log_id),
                             "send_time": "".format(today),
                             "checksum": "",
                             "signature": "",
                             "exts": {"sender_lang": "zh-CN"}},
                  "bodys": [{"version": 1,
                             "trns_type": "DL.001",
                             "trns_id": "".format(trns_id),
                             "crt_time": "".format(today),
                             "exts": {"username": username}
                             }
                            ]
                  }
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/49.0.2623.110 Safari/537.36",
               "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
               "X-Requested-With": "XMLHttpRequest"
               }

    login = requests.post(url=url, headers=headers, data={'message': json.dumps(login_data)})
    if login.status_code == 200:
        return [True, 'SESSION={}'.format(dict(login.cookies)['SESSION'])]
    else:
        return [False, login.content]


# 执行新渠道接口测试
def platform_runner(username, url, params: tuple, start_date, end_date, one_day, page_size, operator, db: Session):
    res = db.query(DApiModule.id, DApiModule.name, DApiModule.method, DApiModule.variable, DApiModule.headers,
                   DApiModule.params, DApiModule.form_data, DApiModule.module_key). \
        filter(DApiModule.is_delete == 0, DApiModule.id.in_(params)).all()
    get_token = platform_login(username, url)
    if get_token[0] is True:
        today = datetime.datetime.today()
        search_day = str(datetime.date.today())
        msg_id = str(uuid.uuid4()).replace('-', '')
        log_id = str(uuid.uuid4()).replace('-', '')
        trns_id = str(uuid.uuid4()).replace('-', '')
        for item in res:
            sys_id = db.query(DSystemModule.name, DModuleModule.name.label('mod_name')). \
                join(DModuleModule, DSystemModule.id == DModuleModule.sys_key). \
                filter(DSystemModule.id == item.module_key).one_or_none()
            db.add(DTaskResultModule(sys_name=sys_id.name, sys_module=sys_id.mod_name, sys_api=item.name,
                                     status='创建'))

            replace_dict = {'START-DATE': start_date, 'END-DATE': end_date, 'ONE-DAY': one_day, 'TODAY': search_day}
            temp_form_data = item.form_data
            temp_headers = eval(item.headers)
            temp_headers['Cookie'] = get_token[1]
            if item.params is not None:
                pass
            if item.form_data is not None:
                for key, value in replace_dict.items():
                    temp_form_data = temp_form_data.replace(key, value)
            if item.method == 'GET':
                pass
            elif item.method == 'POST':
                # pattern = re.compile(r'\$[a-zA-Z0-9]\w+\$')
                # result1 = pattern.findall('$asd$ $asdv$ $12$ $a123$ $12aaaa$')
                data_body = eval(temp_form_data)
                data_body['header']['msg_id'] = msg_id
                data_body['header']['log_id'] = log_id
                data_body['header']['send_time'] = today
                data_body['bodys'][0]['trns_id'] = trns_id
                data_body['bodys'][0]['crt_time'] = today
                if temp_form_data.find('page_size') != -1:
                    data_body['bodys'][0]['exts']['query_paged_cond']['page_size'] = page_size
                response = requests.post(url=url,
                                         data=data_body,
                                         headers=temp_headers
                                         )


@app.task
def taskA(x, y):
    return x + y


@app.task
def taskB(x, y, z):
    return x + y + z


@app.task
def add(x, y):
    return x + y