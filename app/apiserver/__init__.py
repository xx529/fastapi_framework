from app.apiserver.server import HangServer
from app.apiserver.exception import AppException

myapp = HangServer.create_app()
