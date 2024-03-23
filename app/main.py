from loguru import logger
import logging

# logger.add(BASE_DIR/'run.log', serialize='json')


class InterceptHandler(logging.Handler):
    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelname, record.getMessage())


logger_name_list = [name for name in logging.root.manager.loggerDict]

for logger_name in logger_name_list:
    logging.getLogger(logger_name).setLevel(10)
    logging.getLogger(logger_name).handlers = []
    logging.getLogger(logger_name).addHandler(InterceptHandler())


from app.apiserver import myapp

myapp = myapp


if __name__ == '__main__':
    # TODO 启动方式
    import uvicorn
    uvicorn.run(app='main:myapp',
                host='localhost',
                port=8000,
                reload=True,
                app_dir='app',
                workers=5)
