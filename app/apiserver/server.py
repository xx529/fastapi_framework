from fastapi import FastAPI
from app.apiserver.middleware import MiddleWare
from app.router import all_routers
from contextlib import asynccontextmanager
from app.config import AppServerConf, DirConf
from app.apiserver.logger import lifespan_logger


class FastApiServer:

    @classmethod
    def create_app(cls) -> FastAPI:
        app = FastAPI(version=AppServerConf.version,
                      lifespan=cls.lifespan())
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
            app.include_router(r)

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
