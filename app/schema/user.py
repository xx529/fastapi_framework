from typing import Annotated, List, Literal

from pydantic import BaseModel, Field

from app.schema.base import JsonResponse

UserID = Annotated[int, Field(description='用户ID', examples=[123])]
UserName = Annotated[str, Field(description='用户名', examples=['张三'])]
UserAge = Annotated[int, Field(description='用户年龄', examples=[18])]
UserGender = Annotated[Literal['男', '女'], Field(description='用户性别', examples=['男'])]


class UserInfo(BaseModel):
    user_id: UserID
    name: UserName
    age: UserAge
    gender: UserGender


class UserListResponse(JsonResponse):
    data: List[UserInfo] = Field(description='用户列表')
    total: int = Field(description='用户总数')


class UserDetailResponse(JsonResponse):
    data: UserInfo = Field(description='用户详情')


class UserCreateResponse(JsonResponse):
    data: UserID
