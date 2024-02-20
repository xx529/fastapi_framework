from enum import Enum

from pydantic import BaseModel


class DataType(str, Enum):
    start = 'start'
    middle = 'middle'
    end = 'end'


class BaseData(BaseModel):
    type: DataType
    data: dict


class StartData(BaseData):
    type: DataType = DataType.start


class MiddleData(BaseData):
    type: DataType = DataType.middle


class EndData(BaseData):
    type: DataType = DataType.end
