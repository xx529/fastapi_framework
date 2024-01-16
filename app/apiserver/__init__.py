from app.apiserver.server import HangServer
from app.apiserver.logger import runtime_log
from app.apiserver.exception import AppException

myapp = HangServer.create_app()
