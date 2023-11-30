from pydantic import BaseModel
from app.schema.base import DictResponse


class UserInfo(BaseModel):
    user_id: int
    name: str
    city: str
    age: int


class UserInfoForList(BaseModel):
    user_id: int
    name: str


class UserInfoForCreate(BaseModel):
    user_id: int


class UserListResponse(DictResponse):
    data: list[UserInfoForList]


class UserDetailResponse(DictResponse):
    data: UserInfo


class CreateUserResponse(DictResponse):
    data: UserInfoForCreate
