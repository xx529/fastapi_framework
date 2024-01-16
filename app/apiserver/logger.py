import sys

from loguru import logger

from app.config import log_conf, app_conf
from .context import RequestCtx

logger.remove()

FULL_FORMAT = '{time:YYYY-MM-DD HH:mm:ss.SSS} {extra[project_name]} [PID:{process}] [TID:{thread}] [{level}] [{file.path}:{function}:{line}] - [RID:{extra[request_id]}] [TYPE:{extra[type]}] {message}'
SHORT_FORMAT = '[{time:HH:mm:ss.SSS}] [RID:{extra[request_id]}] [{level}] [TYPE:{extra[type]}] {message}'


def patch_request_id(record):
    record['extra'].update(request_id=RequestCtx.get_request_id())


logger.add(sink=log_conf.file,
           format=FULL_FORMAT,
           level='DEBUG',
           serialize=False)

logger.add(sink=sys.stdout,
           format=SHORT_FORMAT,
           level='DEBUG')

_logger = logger.patch(patch_request_id).bind(project_name=app_conf.name)

runtime_log = _logger.bind(type='runtime')
lifespan_log = _logger.bind(type='lifespan')
database_log = _logger.bind(type='database')
