from pydantic import BaseModel
from app.schema.base import DictResponse


class UserInfo(BaseModel):
    id: int
    name: str
    city: str
    age: int


class UserInfoForList(BaseModel):
    id: int
    name: str


class UserListResponse(DictResponse):
    data: list[UserInfoForList]


class UserResponse(DictResponse):
    data: UserInfo
