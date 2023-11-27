from app.apiserver.server import FastApiServer
from app.apiserver.logger import service_logger, request_logger

myapp = FastApiServer.create_app()

slog = service_logger
rlog = request_logger
