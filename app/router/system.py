from fastapi import APIRouter
from app.schema.base import StrResponse, HtmlResponse
from app.service.system import LogService

router = APIRouter(prefix='/system', tags=['system'])


@router.get(path='/health', response_model=StrResponse, summary='健康检查')
async def health():
    return StrResponse(data='ok')


@router.get(path='/log/lifespan', summary='启停日志')
async def log_lifespan():
    data = LogService.life_log_records()
    return HtmlResponse(content=data)


