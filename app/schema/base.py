from typing import Any
from pydantic import BaseModel
from fastapi.responses import HTMLResponse


class BaseResponse(BaseModel):
    errcode: int = 0
    errmsg: str = ''
    detail: str = ''
    data: Any = None


class DictResponse(BaseResponse):
    data: dict


class StrResponse(BaseResponse):
    data: str


class HtmlResponse(HTMLResponse):
    status_code = 200
