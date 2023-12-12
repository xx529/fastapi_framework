from typing import Annotated, Any, Literal

from fastapi import Header
from fastapi.responses import HTMLResponse
from pydantic import BaseModel


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
    data: Literal["ok"] = 'ok'


class HtmlResponse(HTMLResponse):
    status_code = 200


class HeadersParam(BaseModel):
    token: str
    task_id: int
    phone: str


class HeaderParamType:
    Token = Annotated[str, Header(description="用户Token", example="test-token")]
    TaskID = Annotated[int, Header(description="任务ID", example=10)]
    Phone = Annotated[str, Header(description="手机号", example="13800138000")]


def get_common_headers(token: HeaderParamType.Token,
                       task_id: HeaderParamType.TaskID,
                       phone: HeaderParamType.Phone):
    return HeadersParam(token=token, task_id=task_id, phone=phone)
