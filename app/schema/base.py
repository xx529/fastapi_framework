from enum import Enum
from typing import Annotated, Any, Literal

from fastapi import Header, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field


class BaseResponse(BaseModel):
    errcode: int = 0
    errmsg: str = ''
    detail: str = ''
    data: Any = ...


class JsonResponse(BaseResponse):
    data: dict | list


class StrResponse(BaseResponse):
    data: str


class OkResponse(BaseResponse):
    data: Literal["ok"] = 'ok'


class BoolResponse(BaseResponse):
    data: bool = Field(description="成功: true，失败: false", examples=[True])


class NullResponse(BaseResponse):
    data: None = Field(default=None, description="空返回", examples=[None])


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


class PageQueryParams:
    Page = Annotated[int, Query(description="页码", example=1, alias="page")]
    Limit = Annotated[int, Query(description="每页数量", example=10, alias="limit")]
    Search = Annotated[str, Query(description="搜索关键字", example="张三", alias="search")]

    @staticmethod
    def get_page_query_params(page: Page = None,
                              limit: Limit = None,
                              search: Search = None):
        return {'page': page, 'limit': limit, 'search': search}


class PullDataFormat(str, Enum):
    RAW = 'RAW'
    PANDAS = 'PANDAS',
    RECORDS = 'RECORDS'
    PYDANTIC = 'PYDANTIC'
