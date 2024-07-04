from typing import Any, Literal

from pydantic import BaseModel, Field
from starlette.responses import HTMLResponse

from app.apiserver.context import RunContext


class BaseResponse(BaseModel):
    trace_id: str | None = Field(RunContext.current().get_trace_id, description='追踪ID')
    errcode: int = Field(0, description='错误码')
    errmsg: str = Field('', description='错误信息')
    detail: str = Field('', description='错误详情')
    data: Any = Field(..., description='返回的数据')


class JsonResponse(BaseResponse):
    data: dict | list = Field(..., description='返回 json 类型数据')


class StrResponse(BaseResponse):
    data: str = Field(..., description='返回 string 类型数据')


class OkResponse(BaseResponse):
    data: Literal['ok'] = Field('ok', description='返回 ok 字符串')


class BoolResponse(BaseResponse):
    data: bool = Field(description='成功: true，失败: false')


class NullResponse(BaseResponse):
    data: None = Field(default=None, description='空返回')


class HtmlResponse(HTMLResponse):
    status_code = 200
