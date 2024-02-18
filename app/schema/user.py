from typing import List

from pydantic import BaseModel, Field

from app.schema.base import JsonResponse, UserAge, UserGender, UserID, UserName


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
