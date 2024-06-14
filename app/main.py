from app.apiserver import myapp
from app.config import config

myapp = myapp

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app='main:myapp',
                host=config.app_conf.host,
                port=config.app_conf.port,
                reload=config.app_conf.reload,
                app_dir='app',
                workers=config.app_conf.workers)
