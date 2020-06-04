from datetime import datetime, timedelta
import jwt
from fastapi import Depends, FastAPI, HTTPException # , status
from starlette import status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext # passlib 处理哈希加密的包
from pydantic import BaseModel
"""
前端：js vue element-ui

github地址：https://github.com/pencil1/ApiTestWeb

后端：python flask httprunner

github地址： https://github.com/pencil1/ApiTestManage"""


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# verify_password验证密码   plain_password普通密码      hashed_password哈希密码
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# 获取密码哈希
def get_password_hash(password):
    return pwd_context.hash(password)


def mu():
    x = 2
    try:
        y = x / 3
        return y
    except Exception as e:
        return e
    finally:
        print('last')

if __name__ == "__main__":

    print(mu())
    print(datetime.now())
    ############################本章节哈希验证用法############################
    # xxx = get_password_hash('cccccc')
    # yyy = get_password_hash('cccccc')
    # print(xxx)
    # # print(yyy)
    # print('verify_password',verify_password('cccccc',xxx))
    # # print('verify_password',verify_password('cccccc',yyy))
    # print('verify_password',verify_password('cccccc','$2b$12$v.SJbpgmQcNdcqWzLeTbCeH73F0DRNctKXfnoYE3Q9XzP6zHlDn4e'))



    # ############################本章节时间差（timedelta）用法###########################
    # from datetime import datetime
    # from datetime import timedelta
    # aDay = timedelta(minutes=30) # timedelta表示两个datetime对象之间的差异。（来自datetime包）
    # now = datetime.now() + aDay
    # print(aDay)
    # print(datetime.now())
    # print(now ,type(now))