from fastapi import APIRouter, Depends

from app.interface.api.myapp import SelfServiceAPI
from app.schema.response.base import HtmlResponse, OkResponse
from app.schema.schemas.system import LogDetailParam, LogRequestParam
from app.service.system_service import LogService

router = APIRouter(prefix='/system', tags=['系统信息模块'])


@router.get(path='/health/heartbeat',
            summary='健康检查',
            response_model=OkResponse)
async def health():
    return OkResponse()


@router.get(path='/log', summary='请求日志')
async def log_request(param: LogRequestParam = Depends()):
    data = LogService().request_log(refresh=param.refresh,
                                    method=param.method,
                                    status_code=param.status_code,
                                    url_match=param.url_match,
                                    last=param.last)

    return HtmlResponse(content=data)


@router.get(path='/log/{trace_id}', summary='追踪日志')
def log_request_detail(param: LogDetailParam = Depends()):
    data = LogService().runtime_log(param=param)
    return HtmlResponse(content=data)


@router.get(path='/error/demo',
            summary='测试报错')
async def error_demo():
    # num = random.random()
    # raise AppException.Random(detail='this is random')
    # 1 / 0
    # return StrResponse(data='ok')
    ...


@router.get(path='/config',
            summary='当前运行配置信息')
async def config():
    return '1'


@router.get(path='/test')
async def test():
    await SelfServiceAPI.test_api()
    return OkResponse()


@router.get(path='/test_get')
async def test_get():
    return OkResponse()
