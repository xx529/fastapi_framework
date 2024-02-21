from fastapi import APIRouter, Depends

from app.schema.base import HtmlResponse, OkResponse
from app.schema.schemas.system import LogDetailQuery, LogRequestQuery
from app.service.system_service import LogService

router = APIRouter(prefix='/system', tags=['系统信息模块'])


@router.get(path='/health/heartbeat',
            summary='健康检查',
            response_model=OkResponse)
async def health():
    return OkResponse()


@router.get(path='/log', summary='请求日志')
async def log_request(query: LogRequestQuery = Depends()):
    data = LogService().request_log(refresh=query.refresh,
                                    method=query.method,
                                    status_code=query.status_code,
                                    url_match=query.url_match,
                                    last=query.last)

    return HtmlResponse(content=data)


@router.get(path='/log/{request_id}', summary='运行日志')
def log_request_detail(query: LogDetailQuery = Depends()):
    data = LogService().runtime_log(query=query)
    return HtmlResponse(content=data)


@router.get(path='/error/demo',
            summary='测试报错')
async def error_demo():
    # num = random.random()
    # raise AppException.Random(detail='this is random')
    1 / 0
    # return StrResponse(data='ok')


@router.get(path='/config',
            summary='当前运行配置信息')
async def config():
    return '1'
