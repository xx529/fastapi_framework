from typing import NewType
from uuid import UUID

from fastapi import Header, Query
from pydantic import BaseModel
from pydantic.dataclasses import dataclass

from app.schema.const import OrderTypeEnum

UserID = NewType('UserID', int)
TaskID = NewType('TaskID', int)
CompanyID = NewType('CompanyID', int)
Token = NewType('Token', UUID)
TraceID = NewType('TraceID', UUID)
Page = NewType('page', int)
Limit = NewType('limit', int)
OrderBy = NewType('OrderBy', str)
Search = NewType('Search', str)


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
    order_type: OrderTypeEnum = Query(default='asc', title='排序方式', description=OrderTypeEnum.comment(), example='asc',
                                      alias='order_type')
