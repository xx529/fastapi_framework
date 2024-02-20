from dataclasses import dataclass
from typing import Annotated, Any, Literal
from uuid import UUID

from fastapi import Header, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from app.apiserver.context import RequestCtx
from app.schema.enum import OrderTypeEnum

UserID = Annotated[int, Field(title='用户ID', description='用户ID', examples=[1])]
UserName = Annotated[str, Field(title='用户名', description='用户名', examples=['张三'])]
UserAge = Annotated[int, Field(title='用户年龄', description='用户年龄', examples=[18])]
UserGender = Annotated[Literal['男', '女'], Field(title='用户性别', description='用户性别', examples=['男'])]

TaskID = Annotated[int, Field(title='任务ID', description='任务ID', example=1)]
TaskName = Annotated[str, Field(title='任务名称', description='任务名称', example='任务1', min_length=1)]

Token = Annotated[UUID, Header(description='用户Token', example='a85753bc-7a9e-4ff0-b946-b5117352b12c', alias='Token')]
CompanyID = Annotated[str, Header(description='公司ID', example='10', alias='CompanyId')]

Test = Annotated[str, Query(description='test', example='abc', alias='Test')]


class BaseResponse(BaseModel):
    request_id: UUID = Field(default_factory=RequestCtx.get_request_id, description='请求ID')
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
    token: Annotated[str, Header(description='用户Token', example='test-token', alias='Token')]
    task_id: Annotated[int, Header(description='任务ID', example=10, alias='TaskId')]
    company_id: Annotated[str, Header(description='公司ID', example='10', alias='CompanyId')]


@dataclass
class PageQueryParams:
    page: Annotated[int, Query(description='页码', example=1, alias='page')]
    limit: Annotated[int, Query(description='每页数量', example=10, alias='limit')]
    search: Annotated[str, Query(description='搜索关键字', example='张三', alias='search')]
    order_by: Annotated[str, Query(description='排序字段', example='id', alias='order_by')]
    order_type: Annotated[OrderTypeEnum, Query(description='排序方式', example='asc', alias='order_type')]
