import json
import uuid
from contextlib import asynccontextmanager

import fastapi
from fastapi import FastAPI
from loguru import logger

from app.apiserver.logger import lifespan_log
from app.apiserver.middleware import MiddleWare
from app.config import config
from app.interface.cache.redis import redis_cache
from app.interface.mq.kafka import KafkaConsumerManager, KafkaProducerManager
from app.interface.models import close_all_connection, create_all_pg_tables
from app.router import all_routers


class HangServer:

    @classmethod
    def create_app(cls) -> FastAPI:
        app = FastAPI(version=config.app_conf.version, lifespan=cls.lifespan())
        cls.init_middlewares(app)
        cls.init_routers(app)
        cls.config_openapi(app)
        return app

    @staticmethod
    def config_openapi(app: FastAPI):
        openapi_schema = app.openapi()
        openapi_schema['servers'] = [{'url': f'http://127.0.0.1:{config.app_conf.port}', 'description': 'local'}]
        with open('openapi.json', 'w') as f:
            json.dump(openapi_schema, f, indent=4)

    @staticmethod
    def init_middlewares(app: FastAPI) -> None:
        for m in MiddleWare.get_all_middleware():
            app.middleware('http')(m)

    @staticmethod
    def init_routers(app: FastAPI) -> None:
        for r in all_routers:
            app.include_router(r, prefix=config.app_conf.prefix)

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
        for d in config.project_dir.check_create_ls():
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
        KafkaProducerManager.startup()
        KafkaConsumerManager.startup()

    @staticmethod
    async def on_shutdown() -> None:
        lifespan_log.info('shutdown redis')
        await redis_cache.shutdown()

        lifespan_log.info('close all pg connections')
        close_all_connection()

        lifespan_log.info('shutdown kafka')
        KafkaProducerManager.shutdown()
        KafkaConsumerManager.shutdown()
