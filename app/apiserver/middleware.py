import uuid

from starlette.requests import Request

from app.schema.enum import RequestSuccessCode
from .context import RequestCtx
from .logger import runtime_log


class MiddleWare:

    @staticmethod
    async def set_ctx(request: Request, call_next):
        RequestCtx.set_request_id(uuid.uuid4())
        runtime_log.debug(f'set request id: {RequestCtx.get_request_id()}')
        response = await call_next(request)
        return response

    @staticmethod
    async def log_request(request: Request, call_next):
        # TODO 记录服务日志开始

        runtime_log.info(f'{request.method} {request.url}')
        runtime_log.debug(f'headers: {dict(request.headers)}')
        response = await call_next(request)

        if response.status_code in RequestSuccessCode.list():
            runtime_log.info(f'status code: {response.status_code}')
        else:
            runtime_log.error(f'status code: {response.status_code}')

        # TODO 记录服务日志结束
        return response

    @classmethod
    def get_all_middleware(cls):
        mls = [cls.set_ctx, cls.log_request]
        return mls[::-1]
