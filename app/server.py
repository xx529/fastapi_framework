from fastapi import FastAPI
from middleware import MiddleWare
from router import all_routers
from contextlib import asynccontextmanager


class FastApiServer:

    def __init__(self, version):
        self.version = version

    def create_app(self) -> FastAPI:
        app = FastAPI(version=self.version,
                      lifespan=self.lifespan())
        self.init_middlewares(app)
        self.init_routers(app)
        return app

    @staticmethod
    def init_middlewares(app: FastAPI):
        for m in MiddleWare.get_all_middleware():
            app.middleware('http')(m)

    @staticmethod
    def init_routers(app: FastAPI):
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
    def on_start(app: FastAPI):
        print(f'start {app.version}')

    @staticmethod
    def on_shutdown(app: FastAPI):
        print(f'shutdown {app.version}')
