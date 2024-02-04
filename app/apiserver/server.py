import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.apiserver.context import RequestCtx
from app.apiserver.logger import lifespan_log
from app.apiserver.middleware import MiddleWare
from app.config import app_conf, project_dir
from app.interface.cache.redis import redis_cache
from app.interface.repo._base import close_all_connection, create_all_pg_tables
from app.router import all_routers


class HangServer:

    @classmethod
    def create_app(cls) -> FastAPI:
        cls.init_kafka()
        app = FastAPI(version=app_conf.version,
                      lifespan=cls.lifespan())
        cls.init_middlewares(app)
        cls.init_routers(app)
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
        for r in all_routers:
            app.include_router(r, prefix=app_conf.prefix)

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

        lifespan_log.info('close all pg connections')
        close_all_connection()

        lifespan_log.info(f'shutdown api server version: {app.version}')
        # TODO 关闭异步任务
