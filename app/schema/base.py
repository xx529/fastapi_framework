from typing import Any
from pydantic import BaseModel
from fastapi.responses import HTMLResponse


class ExceptionMsg(BaseModel):
    errcode: int
    errmsg: str


class BaseResponse(BaseModel):
    errcode: int = 0
    errmsg: str = ''
    detail: str = ''
    data: Any = None


class DictResponse(BaseResponse):
    data: dict


class StrResponse(BaseResponse):
    data: str


class OkResponse(BaseResponse):
    data: str = 'OK'


class HtmlResponse(HTMLResponse):
    status_code = 200
