import random
from uuid import UUID

from fastapi import APIRouter, Path, Query

from app.apiserver.exception import AppException
from app.schema.base import HtmlResponse, StrResponse
from app.service.system_service import LogService

router = APIRouter(prefix='/system', tags=['系统信息模块'])


@router.get(path='/health/heartbeat',
            summary='健康检查',
            response_model=StrResponse)
async def health(
        num: int = Query(description='测试参数')
):
    return StrResponse(data=str(num))


@router.get(path='/log/lifespan',
            summary='启停日志')
async def log_lifespan():
    data = LogService.life_log_records()
    return HtmlResponse(content=data)


@router.get(path='/log/service',
            summary='请求日志')
def log_service(
        last: int = Query(default=10, description='最近N条记录', ge=1),
        resp_code: int = Query(default=None, description='筛选响应状态码记录', example=200),
):
    return last


@router.get(path='/log/service/{request_id}',
            summary='运行日志')
def log_service_detail(
        request_id: UUID = Path(description='请求ID', example='6fd471a0-101f-4dfb-be22-f36bbaae2905')
):
    return request_id


@router.get(path='/error/demo',
            summary='测试报错')
async def error_demo():
    num = random.random()
    if num > 0.8:
        raise AppException.Demo(detail='this is demo')
    if num > 0.4:
        raise AppException.Random(detail='this is random')
    return StrResponse(data='ok')


@router.get(path='/config',
            summary='当前运行配置信息')
async def config():
    return '1'
