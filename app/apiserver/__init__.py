from app.apiserver.server import HangServer
from app.apiserver.logger import service_logger, request_logger
from app.apiserver.exception import AppException

myapp = HangServer.create_app()

slog = service_logger
rlog = request_logger
