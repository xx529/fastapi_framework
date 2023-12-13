from typing import Annotated, Any, Literal

from fastapi import Header, HTTPException
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


class CommonHeaders(BaseModel):
    token: str
    task_id: int
    phone: str | None = None


class HeaderParams:
    Token = Annotated[str, Header(description="用户Token", example="test-token")]
    TaskID = Annotated[int, Header(description="任务ID", example=10)]
    Phone = Annotated[str, Header(description="手机号", example="13800138000")]

    @staticmethod
    def get_token(token: Token) -> Token:
        return token

    @staticmethod
    def get_task_id(task_id: TaskID) -> TaskID:
        return task_id

    @staticmethod
    def get_phone(phone: Phone) -> Phone:
        return phone

    @staticmethod
    def get_common_headers(token: Token,
                           task_id: TaskID,
                           phone: Phone = None) -> dict:

        return dict(token=token, task_id=task_id, phone=phone)
