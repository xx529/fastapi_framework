from typing import Annotated

from fastapi import Header
from pydantic import BaseModel, Field

from app.schema.base import DictResponse

UserId = Annotated[int, Field(description="用户ID", example=1)]
UserName = Annotated[str, Field(description="用户名", example="张三")]
UserCity = Annotated[str, Field(description="用户城市")]
UserAge = Annotated[int, Field(description="用户年龄")]


class UserInfo(BaseModel):
    user_id: UserId
    name: UserName
    city: UserCity
    age: UserAge


class UserInfoForList(BaseModel):
    user_id: UserId
    name: UserName


class UserInfoForCreate(BaseModel):
    user_id: UserId


class UserListQuery:
    # page: int = Field(default=1, description="页码", ge=1, example=1)
    # limit: int = Field(default=10, description="每页数量", ge=1, example=10)

    page: Annotated[int, Header(description="页码", ge=1, example=1)]


class UserListResponse(DictResponse):
    data: list[UserInfoForList] = Field(description="用户列表")


class UserDetailResponse(DictResponse):
    data: UserInfo


class CreateUserResponse(DictResponse):
    data: UserInfoForCreate
