import os
import platform
import sys
from pathlib import Path

from dynaconf import Dynaconf

current_dir = Path(__file__).parent

files = ['general.yaml', '*.env']

settings = Dynaconf(root_path=current_dir,
                    envvar_prefix='APP',
                    settings_files=files,
                    load_dotenv=True,
                    lowercase_read=True,
                    merge_enabled=True)


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


class PgDataBaseConf:
    host: str = settings.pg.host
    port: int = settings.pg.port
    user: str = settings.pg.user
    password: str = settings.pg.password
    database: str = settings.pg.database
    schema: str = settings.pg.schema
    jdbcurl: str = f'postgresql://{host}:{port}/{database}?user={user}&password={password}'


class SystemInfo:
    python: str = sys.version
    operation: str = sys.platform
    cpus: int = os.cpu_count()
    arch: str = platform.machine()


class AppServerConf:
    version: str = settings.VERSION
    host: str = settings.appserver.host
    port: int = settings.appserver.port
    prefix: str = '/api/v1'


class Resource:
    demo: Path = DirConf.resource / 'demo.txt'


class MyAppApiConf:
    protocol: str = settings.external_api.myapp.protocol
    host: str = settings.external_api.myapp.host
    port: int = settings.external_api.myapp.port
    prefix: str = settings.external_api.myapp.prefix

    @classmethod
    def url(cls, endpoint):
        return f'{cls.protocol}://{cls.host}:{cls.port}{cls.prefix}{endpoint}'
