from typing import Any, Annotated
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi import Header


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


class Headers:
    task: Annotated[int, Header(description="任务ID")]
    phone: Annotated[str, Header(description="手机号")]
