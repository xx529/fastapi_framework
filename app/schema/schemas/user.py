from dataclasses import dataclass
from typing import List, Literal, Annotated

from fastapi import Query
from pydantic import BaseModel, Field

from app.schema.base import JsonResponse, OpenApiExample, UserID

UserIdField = Annotated[UserID, Field(title='用户ID', description='用户ID', examples=[1])]


class UserInfoBase(BaseModel):
    name: str = Field(title='用户名', description='用户名', examples=['张三'])
    age: int = Field(title='用户年龄', description='用户年龄', examples=[18])
    gender: Literal['男', '女'] = Field(title='用户性别', description='用户性别', examples=['男'])


class UserInfo(UserInfoBase):
    user_id: UserIdField


class UserListResponse(JsonResponse):
    data: List[UserInfo] = Field(description='用户列表')
    total: int = Field(description='用户总数')


@dataclass
class UserDetailQuery:
    user_id: UserID = Query(title='用户ID', description='用户ID', ge=0, examples=[1])


class UserDetailResponse(JsonResponse):
    data: UserInfo = Field(description='用户信息详情')


class UserCreateBody(UserInfoBase):
    ...

    @classmethod
    def openapi_examples(cls):
        return {
            "例子1": OpenApiExample(
                summary='例子1（适用于开发环境）',
                description='一般例子1',
                value=cls(name='张三', age=30, gender='男').model_dump(),
            ),
            "例子2": OpenApiExample(
                summary='例子2',
                description='一般例子2',
                value=cls(name='张三', age=28, gender='女').model_dump(),
            )
        }


class UserCreateResponse(JsonResponse):
    data: UserIdField


class UserDeleteBody(BaseModel):
    user_id: UserIdField


class UserUpdateBody(UserInfo):
    ...

    @classmethod
    def openapi_examples(cls):
        ...
