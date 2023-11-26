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
    resource: Path = app / 'resource'


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
