import shutil
import uuid
from pathlib import Path
from typing import Dict, List

from loguru import logger
from pydantic import BaseModel


class ObsFile(BaseModel):
    name: str
    url: str


class ObsFileBytes(ObsFile):
    data: bytes


class ObsFileManager:
    CACHE_DIR = Path().absolute()

    def __init__(self, obs_files: List[ObsFile]):
        self.obs_files = obs_files
        self.working_dir = self.CACHE_DIR / uuid.uuid4().hex
        self.file_data: Dict[str, ObsFileBytes] = {}

    def __enter__(self):
        self.download_files_from_obs()
        self.create_working_dir()
        self.save_files_to_working_dir()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.remove_working_dir()

        if exc_type is not None:
            raise exc_val
        return self

    def __getitem__(self, item) -> bytes:
        return self.file_data[item]

    def create_working_dir(self):
        if not self.working_dir.exists():
            logger.info(f'create tmp dir: {self.working_dir}')
            self.working_dir.mkdir()
        else:
            logger.error(f'working dir already exists: {self.working_dir}')
            raise Exception(f'working dir already exists: {self.working_dir}')

    def remove_working_dir(self):
        if self.working_dir.exists():
            logger.info(f'delete tmp dir: {self.working_dir}')
            shutil.rmtree(self.working_dir)
        else:
            logger.info(f'working dir not exists: {self.working_dir}')

    def download_files_from_obs(self) -> List[ObsFileBytes]:
        ...

    def save_files_to_working_dir(self):
        for bytes_data in self.file_data.values():
            with open(self.working_dir / bytes_data.name, 'wb') as f:
                f.write(bytes_data)


with ObsFileManager([ObsFile(name='test1', url='https://www.test.com/test1'),
                     ObsFile(name='test2', url='https://www.test.com/test2')]) as obs_file_manager:
    ...