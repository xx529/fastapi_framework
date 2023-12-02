from fastapi import APIRouter, Depends
from app.schema.base import StrResponse, HtmlResponse
from app.service.system import LogService
from app.dependencies import Depd

router = APIRouter(prefix='/system', tags=['系统信息模块'])


@router.get(path='/health',
            summary='健康检查',
            response_model=StrResponse)
async def health(d: str = Depends(Depd.error_dep)):
    d
    return StrResponse(data='ok')


@router.get(path='/log/lifespan',
            summary='启停日志')
async def log_lifespan():
    data = LogService.life_log_records()
    return HtmlResponse(content=data)
