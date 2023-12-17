from app.apiserver.server import FastApiServer
from app.apiserver.logger import service_logger, request_logger
from app.apiserver.exception import CommonException

myapp = FastApiServer.create_app()

log = service_logger
rlog = request_logger
