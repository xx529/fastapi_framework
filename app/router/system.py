from fastapi import APIRouter
from app.schema.base import StrResponse, HtmlResponse, DictResponse
import pandas as pd

router = APIRouter(prefix='/system', tags=['system'])


@router.get(path='/health', response_model=StrResponse, summary='健康检查')
async def health():
    return StrResponse(data='ok')


@router.get(path='/log', summary='服务请求日志')
async def log():
    return HtmlResponse(content=pd.DataFrame([1, 2, 3, 4]).to_html())


@router.get(path='/config', response_model=DictResponse, summary='系统配置')
async def setting():
    data = {}
    return DictResponse(data=data)
