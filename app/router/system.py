from fastapi import APIRouter
from app.schema.base import StrResponse, HtmlResponse
from app.config import SystemConf
import pandas as pd

router = APIRouter(prefix='/system', tags=['system'])


@router.get(path='/health', response_model=StrResponse, summary='健康检查')
async def health():
    return StrResponse(data='ok')


@router.get(path='/version', response_model=StrResponse, summary='版本号信息')
async def version():
    return StrResponse(data=SystemConf.version)


@router.get(path='/log', summary='服务请求日志')
async def log():
    return HtmlResponse(content=pd.DataFrame([1, 2, 3, 4]).to_html())
