from typing import Annotated

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


class UserListResponse(DictResponse):
    data: list[UserInfoForList] = Field(description="用户列表")


class UserDetailResponse(DictResponse):
    data: UserInfo


class CreateUserResponse(DictResponse):
    data: UserInfoForCreate
