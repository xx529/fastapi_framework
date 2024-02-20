from dataclasses import dataclass
from pathlib import Path
from typing import List
from uuid import UUID

from fastapi import Query

from app.schema.enum import RequestMethod


@dataclass
class LogRequestQuery:
    refresh: bool = Query(default=False, description='刷新缓存', title='刷新缓存')
    method: List[RequestMethod] = Query(default=None, description='请求方法', title='请求方法')
    status_code: List[int] = Query(default=None, description='请求状态码', title='请求状态码')
    url_match: str = Query(default=None, description='请求路径匹配', title='请求路径匹配')
    last: int = Query(default=20, description="查看最近n条记录", title="查看最近n条记录")


@dataclass
class LogDetailQuery:
    refresh: bool = Query(default=False, description='刷新缓存')
    request_id: UUID = Path(description='请求ID', example='6fd471a0101f4dfbbe22f36bbaae2905')
