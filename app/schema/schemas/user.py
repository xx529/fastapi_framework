from dataclasses import dataclass
from typing import Annotated, List

from fastapi import Query
from pydantic import BaseModel, Field

from app.schema.common import UserID
from app.schema.response.base import JsonResponse
from app.schema.const import HumanGender

UserIdField = Annotated[UserID, Field(title='用户ID', description='用户ID', examples=[1])]
UserNameField = Annotated[str, Field(title='用户名', description='用户名', examples=['张三'], min_length=1)]
UserAgeField = Annotated[int, Field(title='用户年龄', description='用户年龄', examples=[18], ge=1)]
UserGenderField = Annotated[HumanGender, Field(title='用户性别', description='用户性别', examples=['男'])]


class UserInfo(BaseModel):
    user_id: UserIdField
    name: UserNameField
    age: UserAgeField
    gender: UserGenderField


class UserListResponse(JsonResponse):
    data: List[UserInfo] = Field(description='用户列表')
    total: int = Field(description='用户总数')


@dataclass
class UserDetailParam:
    user_id: UserID = Query(title='用户ID', description='用户ID', ge=0, examples=[1])


class UserDetailResponse(JsonResponse):
    data: UserInfo = Field(description='用户信息详情')


class UserCreateBody(BaseModel):
    name: UserNameField
    age: UserAgeField
    gender: UserGenderField


class UserCreateResponse(JsonResponse):
    data: UserIdField


class UserDeleteBody(BaseModel):
    user_id: UserIdField


class UserUpdateBody(UserInfo):
    ...
