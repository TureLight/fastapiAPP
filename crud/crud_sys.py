# from sqlalchemy.orm import Session
# from fastapi import Depends
# from models.model_sys import SystemApi, SystemModule, SystemName
# from sqlalchemy import func, or_
# from datetime import datetime
# from schemas.schemas_sys import CreateProjectModel, UpdateProjectModel
#
#
# # 获取系统
# def crud_get_sys(db: Session, sys_name: str):
#     # off_set = int(page_size)*(int(page_num)-1)
#     # limit = int(page_size)
#     res1 = db.query(SystemName.id, SystemName.name).filter(SystemName.is_delete == 0).all()
#     result = db.query(SystemName.name, SystemModule.name, SystemApi.name, SystemApi.method). \
#         join(SystemModule, SystemName.id == SystemModule.sys_key). \
#         join(SystemApi, SystemModule.id == SystemApi.module_key). \
#         filter(SystemName.name == sys_name).all()
#     return {'sys_list': [{"id": item.id, 'name': item.name, 'tester': item.tester,
#                           'virtualenv': item.virtualenv, 'host': item.host
#                           } for item in result
#                          ]
#             }


