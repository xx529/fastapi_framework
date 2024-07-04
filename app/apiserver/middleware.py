import json
import traceback
import uuid

from fastapi.responses import JSONResponse
from starlette.requests import Request

from .context import ContextInfo, RunContext
from .exception import AppError, AppExceptionEnum
from .logger import exception_log, middleware_log, request_finish_log, request_start_log
from ..schema.response.base import BaseResponse


class MiddleWare:

    @staticmethod
    async def set_logger_trace_id(request: Request, call_next):

        _trace_id = request.headers.get('TraceId')
        trace_id = _trace_id if _trace_id is not None else uuid.uuid4(_trace_id).hex

        with RunContext(ctx=ContextInfo(trace_id=trace_id)):
            response = await call_next(request)
            return response

    @staticmethod
    async def log_request(request: Request, call_next):
        request_start_log.info(f'path:` {request.method} {request.url.path}')
        middleware_log.debug(f'headers: \n{json.dumps(dict(request.headers), indent=4)}')
        middleware_log.debug(f'body: \n{(await request.body()).decode("utf-8")}')

        try:
            response = await call_next(request)
            finish_log_msg = f'status code: {response.status_code}'

        except AppError as e:
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
            res = BaseResponse(errcode=AppExceptionEnum.Unknown.value.errcode,
                               errmsg=AppExceptionEnum.Unknown.value.errmsg,
                               detail=AppExceptionEnum.Unknown.value.errmsg,
                               data='')
            response = JSONResponse(status_code=AppExceptionEnum.Unknown.value.status_code, content=res.model_dump())
            exception_log.error(traceback.format_exc())
            finish_log_msg = (f'status code: {response.status_code} '
                              f'error code: {AppExceptionEnum.Unknown.value.errcode} '
                              f'error msg: {type(e).__name__} '
                              f'detail: {str(e)}')

        request_finish_log.info(finish_log_msg)
        return response

    @classmethod
    def get_all_middleware(cls):
        mls = [cls.set_logger_trace_id, cls.log_request]
        return mls[::-1]
