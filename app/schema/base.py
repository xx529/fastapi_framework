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


class CommonHeaders(BaseModel):
    token: str
    task_id: int
    company_id: str


class HeaderParams:
    Token = Annotated[str, Header(description="用户Token", example="test-token", alias="Token")]
    TaskID = Annotated[int, Header(description="任务ID", example=10, alias="TaskId")]
    CompanyID = Annotated[str, Header(description="公司ID", example="10", alias="CompanyId")]

    @staticmethod
    def get_common_headers(token: Token,
                           task_id: TaskID,
                           company_id: CompanyID) -> CommonHeaders:
        return CommonHeaders(token=token, task_id=task_id, company_id=company_id)
