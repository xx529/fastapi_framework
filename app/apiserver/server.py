import uuid
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse

from app.apiserver.context import RequestCtx
from app.apiserver.exception import AppException, AppExceptionClass
from app.apiserver.logger import lifespan_log
from app.apiserver.middleware import MiddleWare
from app.config import app_conf, project_dir
from app.interface.cache.redis import redis_cache
from app.interface.repo._base import create_all_pg_tables
from app.router import all_routers
from app.schema.base import BaseResponse


class HangServer:

    @classmethod
    def create_app(cls) -> FastAPI:
        # cls.init_database()
        cls.init_kafka()
        app = FastAPI(version=app_conf.version,
                      lifespan=cls.lifespan())
        cls.init_middlewares(app)
        cls.init_routers(app)
        cls.init_exception(app)
        return app

    @staticmethod
    def init_kafka() -> None:
        ...

    @staticmethod
    def init_middlewares(app: FastAPI) -> None:
        for m in MiddleWare.get_all_middleware():
            app.middleware('http')(m)

    @staticmethod
    def init_routers(app: FastAPI) -> None:
        base_router = APIRouter(prefix=app_conf.prefix)
        for r in all_routers:
            base_router.include_router(r)
        app.include_router(base_router)

    @staticmethod
    def init_exception(app: FastAPI) -> None:
        @app.exception_handler(AppExceptionClass)
        async def server_exception_handler(request: Request, exc: AppExceptionClass):
            res = BaseResponse(errcode=exc.errcode,
                               errmsg=exc.errmsg,
                               detail=exc.detail,
                               data='')
            return JSONResponse(status_code=exc.status_code,
                                content=res.model_dump())

        @app.exception_handler(Exception)
        async def unknown_exception_handler(request: Request, exc: Exception):
            res = BaseResponse(errcode=AppException.Unknown.value.errcode,
                               errmsg=AppException.Unknown.value.errmsg,
                               detail=AppException.Unknown.value.errmsg,
                               data='')
            return JSONResponse(status_code=AppException.Unknown.value.status_code,
                                content=res.model_dump())

    @classmethod
    def lifespan(cls):

        @asynccontextmanager
        async def __lifespan(app: FastAPI):
            RequestCtx.set_request_id(uuid.uuid4())
            cls.on_start(app)
            yield
            await cls.on_shutdown(app)

        return __lifespan

    @staticmethod
    def on_start(app: FastAPI) -> None:
        lifespan_log.info(f'startup api server version: {app.version}')

        lifespan_log.info('check dirs')
        for d in project_dir.check_create_ls():
            if not d.exists():
                lifespan_log.info(f'create {d}')
                d.mkdir(parents=True)
            else:
                lifespan_log.info(f'exists {d}')

        lifespan_log.info('startup database')
        create_all_pg_tables()

        lifespan_log.info('startup redis')
        redis_cache.startup()

    @staticmethod
    async def on_shutdown(app: FastAPI) -> None:
        lifespan_log.info('shutdown redis')
        await redis_cache.shutdown()

        lifespan_log.info(f'shutdown api server version: {app.version}')
        # TODO 关闭异步任务
