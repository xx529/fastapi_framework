import datetime
import uuid
from contextlib import asynccontextmanager

import fastapi
from fastapi import FastAPI
from loguru import logger

from app.apiserver.logger import lifespan_log
from app.apiserver.middleware import MiddleWare
from app.config import app_conf, project_dir
from app.interface.cache.redis import redis_cache
from app.interface.repo._base import close_all_connection, create_all_pg_tables
from app.router import all_routers


class HangServer:

    @classmethod
    def create_app(cls) -> FastAPI:
        app = FastAPI(version=app_conf.version, lifespan=cls.lifespan())
        cls.init_middlewares(app)
        cls.init_routers(app)
        return app

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
            with logger.contextualize(trace_id=uuid.uuid4().hex):
                cls.on_start(app)
                lifespan_log.info('startup complete')

                yield

                await cls.on_shutdown()
                lifespan_log.info('shutdown complete')

        return __lifespan

    @staticmethod
    def on_start(app: FastAPI) -> None:
        lifespan_log.info(f'fastapi version {fastapi.__version__}')
        lifespan_log.info(f'startup api server version: {app.version}')

        lifespan_log.info('check dirs')
        for d in project_dir.check_create_ls():
            if not d.exists():
                lifespan_log.info(f'create {d}')
                d.mkdir(parents=True)
            else:
                lifespan_log.info(f'exists {d}')

        lifespan_log.info('auto create database table')
        create_all_pg_tables()

        lifespan_log.info('startup redis')
        redis_cache.startup()

        lifespan_log.info('startup kafka')
        ...

    @staticmethod
    async def on_shutdown() -> None:
        lifespan_log.info('shutdown redis')
        await redis_cache.shutdown()

        lifespan_log.info('close all pg connections')
        close_all_connection()

        lifespan_log.info('shutdown kafka')
