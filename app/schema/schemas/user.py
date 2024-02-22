from dataclasses import dataclass
from typing import List

from fastapi import Query
from pydantic import BaseModel, Field

from app.schema.base import JsonResponse, OpenApiExample, UserAge, UserGender, UserID, UserName


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

    @classmethod
    def openapi_examples(cls):
        return {
            "例子1": OpenApiExample(
                summary='例子1',
                description='一般例子1',
                value=cls(name='张三', age=30, gender='男')
            ),
            "例子2": OpenApiExample(
                summary='例子2',
                description='一般例子2',
                value=cls(name='张三', age=28, gender='女')
            )
        }


class UserCreateResponse(JsonResponse):
    data: UserID


class UserDeleteBody(BaseModel):
    user_id: UserID


class UserUpdateBody(BaseModel):
    user_id: UserID
    name: UserName = None
    age: UserAge = None
    gender: UserGender = None
