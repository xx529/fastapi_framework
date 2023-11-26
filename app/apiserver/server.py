from fastapi import FastAPI
from app.apiserver.middleware import MiddleWare
from app.router import all_routers
from contextlib import asynccontextmanager
from app.config import AppServerConf, DirConf


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
        print(f'startup {app.version}')

        dir_ls = [DirConf.data, DirConf.log]
        for d in dir_ls:
            if not d.exists():
                d.mkdir(parents=True)

    @staticmethod
    def on_shutdown(app: FastAPI) -> None:
        print(f'shutdown {app.version}')
