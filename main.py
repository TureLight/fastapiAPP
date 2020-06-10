from fastapi import FastAPI, Header, Depends
from starlette.middleware.cors import CORSMiddleware

from api import user_control, work_report, interface_test, task_manager
from starlette.requests import Request
from starlette.responses import JSONResponse
import jwt
from crud.crud_user_control import get_user
from common.database import get_db


app = FastAPI()

# openssl rand -base64 64
SECRET_KEY = 'N9sbUevTrCkfIWC50PDdyIwJoqHYLq7+duQ9rRdBogTgA/T/9TeDglzDBRrHExROgzvIe4WFPMajNyOn2iEBBA=='
ALGORITHM = 'HS256'
# 过期时间
ACCESS_TOKEN_EXPIRE_MINUTES = 60*12


app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


class TokenError(Exception):
    def __init__(self, name: str):
        self.name = name


@app.exception_handler(TokenError)
async def token_error(request: Request, exc: TokenError):
    return JSONResponse(status_code=200,
                        content={'meta': {'status': 403, 'msg': '{}'.format(exc.name)}})


async def get_token_header(Authorization: str = Header(...), db=Depends(get_db)):
    try:
        payload = jwt.decode(Authorization, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        check = get_user(db=db, accent=username)
        # print(check)
        if check is None:
            raise TokenError(name='token已过期')
    except Exception as e:
        raise TokenError(name=str(e))


app.include_router(user_control.router,
                   prefix='/api',
                   tags=['user'])
app.include_router(work_report.router,
                   prefix='/api/work',
                   tags=['work'],
                   dependencies=[Depends(get_token_header)],
                   # responses={'meta': {'status': 403, 'msg': 'token已过期'}}
                   )
app.include_router(interface_test.router,
                   prefix='/api/interface',
                   tags=['interface'],
                   dependencies=[Depends(get_token_header)],
                   # responses={'meta': {'status': 403, 'msg': 'token已过期'}}
                   )
app.include_router(task_manager.router,
                   prefix='/api/task',
                   tags=['task_manager'],
                   dependencies=[Depends(get_token_header)],
                   # responses={'meta': {'status': 403, 'msg': 'token已过期'}}
                   )


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app='main:app',
                host="192.168.3.2",
                port=8888,
                # reload=True
                )