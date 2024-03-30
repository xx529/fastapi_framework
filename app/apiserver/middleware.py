import json
import traceback

from fastapi.responses import JSONResponse
from loguru import logger
from starlette.requests import Request

from app.schema.base import BaseResponse
from .context import RequestCtx
from .exception import AppException, AppExceptionClass
from .logger import exception_log, middleware_log, request_finish_log, request_start_log


class MiddleWare:

    @staticmethod
    async def set_logger_trace_id(request: Request, call_next):

        trace_id = RequestCtx.create_trace_id()
        with logger.contextualize(trace_id=trace_id):
            response = await call_next(request)
            return response

    @staticmethod
    async def log_request(request: Request, call_next):
        request_start_log.info(f'{request.method} {request.url}')
        middleware_log.debug(f'headers: \n{json.dumps(dict(request.headers), indent=4)}')
        middleware_log.debug(f'body: \n{(await request.body()).decode("utf-8")}')

        try:
            response = await call_next(request)
            finish_log_msg = f'status code: {response.status_code}'

        except AppExceptionClass as e:
            res = BaseResponse(errcode=e.errcode,
                               errmsg=e.errmsg,
                               detail=e.detail,
                               data='')
            response = JSONResponse(status_code=e.status_code, content=res.model_dump())
            finish_log_msg = (f'status code: {response.status_code} '
                              f'error code: {e.errcode} '
                              f'error msg: {e.errmsg} '
                              f'detail: {e.detail}')

        except Exception as e:
            res = BaseResponse(errcode=AppException.Unknown.value.errcode,
                               errmsg=AppException.Unknown.value.errmsg,
                               detail=AppException.Unknown.value.errmsg,
                               data='')
            response = JSONResponse(status_code=AppException.Unknown.value.status_code, content=res.model_dump())
            exception_log.error(traceback.format_exc())
            finish_log_msg = (f'status code: {response.status_code} '
                              f'error code: {AppException.Unknown.value.errcode} '
                              f'error msg: {type(e).__name__} '
                              f'detail: {str(e)}')

        request_finish_log.info(finish_log_msg)
        return response

    @classmethod
    def get_all_middleware(cls):
        mls = [cls.set_logger_trace_id, cls.log_request]
        return mls[::-1]
