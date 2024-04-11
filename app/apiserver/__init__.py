from app.apiserver.server import HangServer
from app.apiserver.exception import AppExceptionEnum

myapp = HangServer.create_app()
