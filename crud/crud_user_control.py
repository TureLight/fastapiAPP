from sqlalchemy.orm import Session
from models.model_user import UserControl
from datetime import datetime, timedelta
import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext  # passlib 处理哈希加密的包


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/token')
# openssl rand -base64 64
SECRET_KEY = 'N9sbUevTrCkfIWC50PDdyIwJoqHYLq7+duQ9rRdBogTgA/T/9TeDglzDBRrHExROgzvIe4WFPMajNyOn2iEBBA=='
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60*12
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# verify_password验证密码   plain_password普通密码      hashed_password哈希密码
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# 获取密码哈希
def get_password_hash(password):
    return pwd_context.hash(password)


# 创建访问令牌
def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta  # expire 令牌到期时间
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def user_menu_dict():
    res = {'data': [{'id': 2, 'auth': '工作日报',
                     'children': [{'id': 21, 'auth': '今日报告', 'path': 'todayWork'},
                                  {'id': 22, 'auth': '历史报告', 'path': 'historyWork'}
                                  ]},
                    {'id': 3, 'auth': '任务管理',
                     'children': [{'id': 31, 'auth': '运行状态', 'path': 'checkTask'},
                                  {'id': 32, 'auth': '配置任务', 'path': 'setTask'},
                                  {'id': 33, 'auth': '结果查询', 'path': 'checkResult'}]
                     },
                    {'id': 4, 'auth': '页面测试',
                     'children': [{'id': 41, 'auth': '新增用例', 'path': 'newWebCase'},
                                  {'id': 42, 'auth': '用例查询', 'path': 'checkWebCase'}]
                     },
                    {'id': 5, 'auth': '接口测试',
                     'children': [{'id': 51, 'auth': '接口项目', 'path': 'interfaceProject'},
                                  {'id': 52, 'auth': '接口用例', 'path': 'interfaceCase'},
                                  {'id': 53, 'auth': '修改用例', 'path': 'editInterfaceCase'}]
                     },
                    {'id': 6, 'auth': '性能测试',
                     'children': [{'id': 61, 'auth': '新增用例', 'path': 'newPerformance'},
                                  {'id': 62, 'auth': '用例查询', 'path': 'checkPerformance'}]
                     },
                    ],
           'meta': {'status': 200,
                    'msg': '菜单列表获取成功'
                    }
           }
    return res


# 检查相同的账号
def check_same_accent(db: Session, accent: str):
    return db.query(UserControl.username, UserControl.password).\
        filter(UserControl.username == accent).one_or_none()


def get_user(db: Session, accent: str):
    return db.query(UserControl.username, UserControl.password, UserControl.name).\
        filter(UserControl.username == accent).one_or_none()


# 注册账号
def register_accent(db: Session, accent: str, password_hash: str, create_time, name: str):
    db.add(UserControl(username=accent, password=password_hash, is_active=0, name=name, create_time=create_time))
    db.commit()
