from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.apiserver.exception import ExceptionClass
from app.apiserver.logger import lifespan_logger
from app.apiserver.middleware import MiddleWare
from app.config import AppServerConf, DirConf
from app.router import all_routers
from app.schema.base import BaseResponse
from app.interface.repo._base import create_all_pg_tables


class FastApiServer:

    @classmethod
    def create_app(cls) -> FastAPI:
        cls.init_database()
        app = FastAPI(version=AppServerConf.version,
                      lifespan=cls.lifespan())
        cls.init_middlewares(app)
        cls.init_routers(app)
        cls.init_exception(app)
        return app

    @staticmethod
    def init_database() -> None:
        create_all_pg_tables()

    @staticmethod
    def init_middlewares(app: FastAPI) -> None:
        for m in MiddleWare.get_all_middleware():
            app.middleware('http')(m)

    @staticmethod
    def init_routers(app: FastAPI) -> None:
        for r in all_routers:
            app.include_router(r)

    @staticmethod
    def init_exception(app: FastAPI) -> None:
        @app.exception_handler(ExceptionClass)
        async def server_exception_handler(request: Request, exc: ExceptionClass):
            res = BaseResponse(errcode=exc.errcode, errmsg=exc.errmsg, detail=exc.detail, data='')
            return JSONResponse(status_code=exc.status_code,
                                content=res.model_dump())

    @classmethod
    def lifespan(cls):

        @asynccontextmanager
        async def __lifespan(app: FastAPI):
            cls.on_start(app)
            yield
            cls.on_shutdown(app)

        return __lifespan

    @staticmethod
    def on_start(app: FastAPI) -> None:
        lifespan_logger.info(f'startup version: {app.version}')

        lifespan_logger.info('check dirs')
        for d in DirConf.check_create_ls():
            if not d.exists():
                lifespan_logger.info(f'create {d}')
                d.mkdir(parents=True)
            else:
                lifespan_logger.info(f'exists {d}')

    @staticmethod
    def on_shutdown(app: FastAPI) -> None:
        lifespan_logger.info(f'shutdown version: {app.version}')
