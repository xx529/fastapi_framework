from dynaconf import Dynaconf
from pathlib import Path
import sys
import os
import platform

current_dir = Path(__file__).parent

files = ['*.yaml']

settings = Dynaconf(root_path=current_dir,
                    settings_files=files,
                    load_dotenv=True,
                    lowercase_read=True)


def load_file(path: Path):
    match path.suffix:
        case '.yaml':
            return None
        case _:
            with open(path) as f:
                return [x.strip() for x in f.readlines()]


class DirConf:
    base: Path = current_dir.parent.parent
    app: Path = base / 'app'
    data: Path = base / 'data'
    log: Path = data / 'log'
    request_log: Path = log / 'request'
    service_log: Path = log / 'service'
    lifespan_log: Path = log / 'lifespan'
    resource: Path = app / 'resource'

    @classmethod
    def check_create_ls(cls):
        return [cls.request_log, cls.service_log, cls.lifespan_log]


class LogConf:
    request_name: str = 'request'
    request_format: str = '{time:YYYY-MM-DD HH:mm:ss} | {thread.name} | {level} | {message}'
    request_file: Path = DirConf.request_log / 'request.log'

    service_name: str = 'service'
    service_format: str = '{time:YYYY-MM-DD HH:mm:ss} | {thread.name} | {level} | {message}'
    service_file: Path = DirConf.service_log / 'service.log'

    lifespan_name: str = 'lifespan'
    lifespan_format: str = '{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}'
    lifespan_file: Path = DirConf.lifespan_log / 'lifespan.log'


class DataBaseConf:
    host: str = 'localhost'
    port: int = '5432'
    user: str = 'postgres'
    password: str = '123456'
    database: str = 'postgres'
    schema: str = 'myapp'
    jdbcurl: str = f'postgresql://{host}:{port}/{database}?user={user}&password={password}'


class SystemInfo:
    python: str = sys.version
    operation: str = sys.platform
    cpus: int = os.cpu_count()
    arch: str = platform.machine()


class AppServerConf:
    version: str = settings.appserver.version
    host: str = settings.appserver.host
    port: int = settings.appserver.port


class Resource:
    demo: Path = DirConf.resource / 'demo.txt'
