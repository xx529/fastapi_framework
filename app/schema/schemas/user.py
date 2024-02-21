from dataclasses import dataclass
from typing import List

from fastapi import Query
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


@dataclass
class UserDetailQuery:
    user_id: int = Query(description='用户ID', ge=0, examples=[1])


class UserDetailResponse(JsonResponse):
    data: UserInfo = Field(description='用户详情')


class UserCreateBody(BaseModel):
    name: UserName
    age: UserAge
    gender: UserGender


class UserCreateResponse(JsonResponse):
    data: UserID


class UserDeleteBody(BaseModel):
    user_id: UserID


class UserUpdateBody(BaseModel):
    user_id: UserID
    name: UserName = None
    age: UserAge = None
    gender: UserGender = None
