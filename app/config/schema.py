import os
import platform
import sys
from pathlib import Path
from typing import Literal

from dynaconf import Dynaconf
from pydantic import BaseModel, Field, model_validator

current_dir = Path(__file__).parent
project_dir = current_dir.parent.parent

files = ['default.yaml',
         '*.yaml'
         '*.env',
         project_dir / 'settings.yaml']

settings = Dynaconf(root_path=current_dir,
                    envvar_prefix='APP',
                    settings_files=files,
                    load_dotenv=True,
                    lowercase_read=True,
                    merge_enabled=True)


class DirConfig(BaseModel):
    root: Path = Field(project_dir, description='项目根目录', const=True)
    app: Path = Field(None, description='程序源码目录', const=True)
    data: Path = Field(None, description='持久化保存的数据目录', const=True)
    log: Path = Field(None, description='日志目录', const=True)
    request_log: Path = Field(None, description='请求日志目录', const=True)
    service_log: Path = Field(None, description='服务日志目录', const=True)
    lifespan_log: Path = Field(None, description='启停日志目录', const=True)
    resource: Path = Field(None, description='资源文件目录', const=True)

    @model_validator(mode='after')
    def set_values(self):
        self.app = self.root / 'app'
        self.data = self.root / 'data'
        self.log = self.data / 'log'
        self.request_log = self.log / 'request'
        self.service_log = self.log / 'service'
        self.lifespan_log = self.log / 'lifespan'
        self.resource = self.app / 'resource'

    def check_create_ls(self):
        return [self.request_log, self.service_log, self.lifespan_log]


class LoggerConfig(BaseModel):
    name: Literal['request', 'service', 'lifespan'] = Field(description='日志名称', const=True)
    format: str = Field(description='日志格式', const=True)
    path: Path = Field(description='日志文件路径', const=True)
    file: Path = Field(None, description='日志文件', const=True)

    @model_validator(mode='after')
    def set_values(self):
        self.file = self.path / f'{self.name}.log'


class GeneralDataBaseConnection(BaseModel):
    host: str = Field(description='地址', const=True)
    port: int = Field(description='端口', const=True)
    user: str = Field(description='用户名', const=True)
    password: str = Field(description='密码', const=True)
    database: str = Field(description='数据库', const=True)
    schema: str = Field(description='schema', const=True)
    jdbcurl: str = Field(None, description='jdbcurl', const=True)

    @model_validator(mode='after')
    def set_values(self):
        self.jdbcurl = f'postgresql://{self.host}:{self.port}/{self.database}?user={self.user}&password={self.password}'


class RedisConnection(BaseModel):
    host: str = Field(description='地址', const=True)
    port: int = Field(description='端口', const=True)
    db: int = Field(description='数据库', const=True)
    password: str = Field(description='密码', const=True)
    max_connections: int = Field(description='最大连接数', const=True)
    project_prefix: str = Field(description='项目前缀', const=True)
    expire_seconds: int = Field(description='默认过期时间', const=True)


class SystemInfo(BaseModel):
    python: str = Field(sys.version, description='python版本', const=True)
    operation: str = Field(sys.platform, description='操作系统', const=True)
    cpus: int = Field(os.cpu_count(), description='cpu核数', const=True)
    arch: str = Field(platform.machine(), description='cpu架构', const=True)


class AppServerConfig(BaseModel):
    version: str = Field(description='服务当前版本', const=True)
    host: str = Field(description='服务地址', const=True)
    port: int = Field(description='服务端口', const=True)
    prefix: str = Field(description='url前缀', const=True)


class ResourceFileConfig(BaseModel):
    path: Path = Field(description='资源文件目录路径', const=True)
    demo: Path = Field(None, description='demo.txt文件', const=True)

    @model_validator(mode='after')
    def set_values(self):
        self.demo = self.path / 'demo.txt'


class MyAppApiConf:
    protocol: str = settings.external_api.myapp.protocol
    host: str = settings.external_api.myapp.host
    port: int = settings.external_api.myapp.port
    prefix: str = settings.external_api.myapp.prefix

    @classmethod
    def url(cls, endpoint):
        return f'{cls.protocol}://{cls.host}:{cls.port}{cls.prefix}{endpoint}'
