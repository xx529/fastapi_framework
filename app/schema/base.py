from dataclasses import dataclass
from typing import Any, Literal, NewType
from uuid import UUID

from fastapi import Header, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from app.apiserver.context import RequestCtx
from app.schema.enum import OrderTypeEnum

UserID = NewType('UserID', int)
TaskID = NewType('TaskID', int)
CompanyID = NewType('CompanyID', int)
Token = NewType('Token', UUID)
RequestID = NewType('RequestID', UUID)
Page = NewType('page', int)
Limit = NewType('limit', int)
OrderBy = NewType('OrderBy', str)
Search = NewType('Search', str)


class BaseResponse(BaseModel):
    request_id: RequestID = Field(default_factory=RequestCtx.get_request_id, description='请求ID')
    errcode: int = Field(0, description='错误码')
    errmsg: str = Field('', description='错误信息')
    detail: str = Field('', description='错误详情')
    data: Any = Field(..., description='返回的数据')


class JsonResponse(BaseResponse):
    data: dict | list = Field(..., description='返回 json 类型数据')


class StrResponse(BaseResponse):
    data: str = Field(..., description='返回 string 类型数据')


class OkResponse(BaseResponse):
    data: Literal['ok'] = Field('ok', description='返回 ok 字符串')


class BoolResponse(BaseResponse):
    data: bool = Field(description='成功: true，失败: false')


class NullResponse(BaseResponse):
    data: None = Field(default=None, description='空返回')


class HtmlResponse(HTMLResponse):
    status_code = 200


@dataclass
class CommonHeaders:
    token: Token = Header(description='用户Token', example='442221ef-38b2-489c-bc46-68d62825ec56', alias='Token')
    company_id: CompanyID = Header(description='公司ID', example='10', alias='CompanyId')


@dataclass
class PageQueryParams:
    page: Page = Query(default=1, description='页码', example=1, alias='page')
    limit: Limit = Query(default=10, description='每页数量', example=10, alias='limit')
    search: Search = Query(default=None, description='搜索关键字', example='张三', alias='search')
    order_by: OrderBy = Query(default='id', description='排序字段', example='id', alias='order_by')
    order_type: OrderTypeEnum = Query(default='asc', title='排序方式', description=OrderTypeEnum.note(), example='asc', alias='order_type')


class OpenApiExample(BaseModel):
    summary: str = None
    description: str = None
    value: dict
