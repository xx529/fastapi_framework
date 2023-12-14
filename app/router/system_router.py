import random

from fastapi import APIRouter, Depends

from app.apiserver.exception import CommonException
from app.dependencies import Depd
from app.schema.base import HtmlResponse, StrResponse
from app.service.system_service import LogService

router = APIRouter(prefix='/system', tags=['系统信息模块'])


@router.get(path='/health',
            summary='健康检查',
            response_model=StrResponse)
async def health(d: str = Depends(Depd.error_dep)):
    return StrResponse(data='ok')


@router.get(path='/log/lifespan',
            summary='启停日志')
async def log_lifespan():
    data = LogService.life_log_records()
    return HtmlResponse(content=data)


@router.get(path='/error/demo',
            summary='测试报错')
async def error_demo():
    num = random.random()
    if num > 0.8:
        raise CommonException.Demo(detail='this is demo')
    if num > 0.4:
        raise CommonException.Random(detail='this is random')
    return StrResponse(data='ok')
