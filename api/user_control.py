from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from common.database import get_db
from schemas.schemas_user import RegisteredForm, LoginForm
from crud.crud_user_control import (get_password_hash,
                                    check_same_accent,
                                    get_user,
                                    register_accent,
                                    create_access_token,
                                    ACCESS_TOKEN_EXPIRE_MINUTES,
                                    verify_password
                                    )
from sqlalchemy.orm import Session


router = APIRouter()


@router.post('/registered/')
async def registered_user(item: RegisteredForm, db: Session = Depends(get_db)):
    db_user = check_same_accent(db, item.username)
    if db_user:
        return {'meta': {'status': 401, 'msg': '账号名称重复,请重新输入!'}}
    else:
        now = datetime.today()
        password = item.password[6:-4]
        hash_password = get_password_hash(password)
        register_accent(db=db, accent=item.username, password_hash=hash_password, create_time=now)
        return {'meta': {'status': 201, 'msg': '注册账号成功,请联系管理员激活账号'}}


# 登录获取令牌
@router.post("/token/")
async def login_for_access_token(form_data: LoginForm, db: Session = Depends(get_db)):
    # 1、验证用户
    password = form_data.password[6:-4]
    check = get_user(db, form_data.username)  # 验证用户
    if check is not None:
        check_pass = verify_password(password, check.password)
        if check_pass:
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(data={"sub": form_data.username},
                                               expires_delta=access_token_expires)
            return {'status': 200, "access": access_token, "username": form_data.username}
        else:
            return {'status': 403, 'msg': '账号或密码错误!'}
    else:
        return {'status': 403, 'msg': '账号不存在或者未激活!'}
