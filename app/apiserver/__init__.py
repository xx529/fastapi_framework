from app.apiserver.server import FastApiServer
from app.apiserver.logger import service_logger, request_logger
from app.apiserver.exception import ServerException

myapp = FastApiServer.create_app()

slog = service_logger
rlog = request_logger
