from typing import Annotated, Literal

from pydantic import BaseModel, Field

from app.schema.base import JsonResponse

UserId = Annotated[int, Field(description='用户ID', examples=[123])]
UserName = Annotated[str, Field(description='用户名', examples=['张三'])]
UserCity = Annotated[str, Field(description='用户城市', examples=['北京'])]
UserAge = Annotated[int, Field(description='用户年龄', examples=[18])]
UserGender = Annotated[Literal['男', '女'], Field(description='用户性别', examples=['男'])]


class UserInfo(BaseModel):
    user_id: UserId
    name: UserName
    city: UserCity
    age: UserAge
    gender: UserGender


class UserInfoForList(BaseModel):
    user_id: UserId
    name: UserName


class UserListResponse(JsonResponse):
    data: list[UserInfoForList] = Field(description='用户列表')


class UserDetailResponse(JsonResponse):
    data: UserInfo = Field(description='用户详情')


class UserCreateResponse(JsonResponse):
    data: UserId
