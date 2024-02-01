import random
from typing import List, Literal
from uuid import UUID

from fastapi import APIRouter, Path, Query

from app.apiserver.exception import AppException
from app.schema.base import HtmlResponse, OkResponse, StrResponse
from app.service.system_service import LogService

router = APIRouter(prefix='/system', tags=['系统信息模块'])


@router.get(path='/health/heartbeat',
            summary='健康检查',
            response_model=OkResponse)
async def health():
    return OkResponse()


@router.get(path='/log/request',
            summary='请求日志')
async def log_request(
        refresh: bool = Query(default=False, description='刷新缓存'),
        method: List[Literal['GET', 'POST', 'PUT', 'DELETE']] = Query(default=None, description='请求方法'),
        code: List[int] = Query(default=None, description='请求状态码'),
        url_match: str = Query(default=None, description='请求路径匹配'),
):
    data = LogService.request_log(refresh=refresh, method=method, code=code, url_match=url_match)
    return HtmlResponse(content=data)


@router.get(path='/log/request/{request_id}',
            summary='运行日志')
def log_request_detail(
        request_id: UUID = Path(description='请求ID', example='6fd471a0101f4dfbbe22f36bbaae2905'),
        refresh: bool = Query(default=False, description='刷新缓存'),

):
    data = LogService.runtime_log(request_id=request_id, refresh=refresh)
    return HtmlResponse(content=data)


@router.get(path='/log/lifespan',
            summary='启停日志')
async def log_lifespan():
    data = LogService.life_log_records()
    return HtmlResponse(content=data)


@router.get(path='/error/demo',
            summary='测试报错')
async def error_demo():
    # num = random.random()
    # raise AppException.Random(detail='this is random')
    1 / 0
    return StrResponse(data='ok')


@router.get(path='/config',
            summary='当前运行配置信息')
async def config():
    return '1'
