import logging
import sys

from loguru import logger


# 创建一个用于将 Python 日志消息重定向到 Loguru 的处理程序
class InterceptHandler(logging.Handler):
    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelname, record.getMessage())


# 配置 Python 的 logging 模块
logging.basicConfig(handlers=[InterceptHandler()], level=logging.DEBUG)

# 启用 Loguru 拦截 Python logging 输出
logger.enable(__name__)

# Loguru 配置示例
logger.add(sys.stdout, level="DEBUG", format="{time} {level} {message}", serialize=True)

# 使用 Python logging 输出日志消息
with logger.contextualize(trace_id=123):
    logging.debug("This is a debug message")
    logging.info("This is an info message")
    logging.warning("This is a warning message")
    logging.error("This is an error message")


from loguru import logger as loguru_logger
from fastapi.logger import logger as fastapi_logger


class InterceptHandler(logging.Handler):
    def emit(self, record):
        loguru_logger.opt(depth=6, exception=record.exc_info).log(record.levelname, record.getMessage())


def setup_logger():
    logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)
    fastapi_logger.handlers = [InterceptHandler()]


setup_logger()