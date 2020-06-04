from typing import List
from pydantic import BaseModel


class RegisteredForm(BaseModel):
    username: str
    password: str
    name: str


class LoginForm(BaseModel):
    username: str
    password: str


class Token(BaseModel):     # 令牌空壳
    access_token: str
    token_type: str


class TokenData(BaseModel):  # 令牌数据
    username: str = None


class User(BaseModel):      # 用户基础模型
    username: str
    is_active: bool = None


class UserInDB(User):       # 用户输入数据模型
    hashed_password: str
    username: str


