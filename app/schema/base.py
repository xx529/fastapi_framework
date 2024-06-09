from typing import Any, List, Literal, NewType
from uuid import UUID

from fastapi import Header, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass

from app.apiserver.context import RequestCtx
from app.schema.enum import KafkaTopic, OrderTypeEnum

UserID = NewType('UserID', int)
TaskID = NewType('TaskID', int)
CompanyID = NewType('CompanyID', int)
Token = NewType('Token', UUID)
TraceID = NewType('TraceID', UUID)
Page = NewType('page', int)
Limit = NewType('limit', int)
OrderBy = NewType('OrderBy', str)
Search = NewType('Search', str)


class BaseResponse(BaseModel):
    trace_id: TraceID | None = Field(default_factory=RequestCtx.get_trace_id, description='追踪ID')
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


class CommonHeaders(BaseModel):
    token: Token
    company_id: CompanyID
    trace_id: TraceID

    @classmethod
    def get_from_header(cls,
                        token: Token = Header(description='用户Token', example='442221ef-38b2-489c-bc46-68d62825ec56',
                                              alias='Token'),
                        company_id: CompanyID = Header(description='公司ID', example='10', alias='CompanyId'),
                        trace_id: TraceID = Header(default=None, description='追踪 ID',
                                                   example='442221ef-38b2-489c-bc46-68d62825ec56')):
        return cls(token=token, company_id=company_id, trace_id=trace_id)


class WithAuthHeaders(CommonHeaders):
    auth: str = Header(description='用户认证信息', example='Bearer token', alias='Authorization')

    @classmethod
    def get_from_header(cls,
                        token: Token = Header(description='用户Token', example='442221ef-38b2-489c-bc46-68d62825ec56',
                                              alias='Token'),
                        company_id: CompanyID = Header(description='公司ID', example='10', alias='CompanyId'),
                        trace_id: TraceID = Header(default=None, description='追踪 ID',
                                                   example='442221ef-38b2-489c-bc46-68d62825ec56'),
                        auth: str = Header(description='用户认证信息', example='Bearer token', alias='Authorization')):
        return cls(token=token, company_id=company_id, trace_id=trace_id, auth=auth)


@dataclass
class PageQueryParams:
    page: Page = Query(default=1, description='页码', example=1, alias='page')
    limit: Limit = Query(default=10, description='每页数量', example=10, alias='limit')
    search: Search = Query(default=None, description='搜索关键字', example='张三', alias='search')
    order_by: OrderBy = Query(default='id', description='排序字段', example='id', alias='order_by')
    order_type: OrderTypeEnum = Query(default='asc', title='排序方式', description=OrderTypeEnum.note(), example='asc',
                                      alias='order_type')


class Example(BaseModel):
    summary: str = Field(description='摘要')
    description: str = Field(description='描述')
    data: BaseModel = Field(description='值')

    def to_openapi(self):
        return {'summary': self.summary, 'description': self.description, 'value': self.data.model_dump()}


class ExampleSet(BaseModel):
    examples: List[Example] = Field(description='OpenAPI示例')

    def to_openapi_examples(self):
        return {example.summary: example.to_openapi() for example in self.examples}


class KafkaMessage(BaseModel):
    trace_id: str | None = Field(default_factory=RequestCtx.get_trace_id, description='来自的追踪ID')
    topic: KafkaTopic = Field(description='消息主题')
    data: Any = Field(description='消息内容')
