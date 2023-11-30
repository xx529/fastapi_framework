from fastapi import APIRouter, Query, Body
from app.schema.user import (
    UserListResponse,
    UserDetailResponse,
    UserInfo,
    CreateUserResponse,
    UserInfoForCreate
)
from app.schema.base import OkResponse
from app.service.user import UserService
from typing import Annotated

router = APIRouter(prefix='/user', tags=['用户管理模块'])


@router.get(
    path='/list',
    summary='获取用户列表',
    description='获取用户列表通用接口',
    response_model=UserListResponse
)
def user_list(
        page: Annotated[int, Query(description='页码', ge=1)] = 1,
        limit: Annotated[int, Query(description='每页数量', ge=1)] = 10
):
    data = UserService.list(page=page, limit=limit)
    return UserListResponse(data=data)


@router.post(
    path='',
    summary='创建用户',
    description='创建用户通用接口',
    response_model=CreateUserResponse
)
def add_user(
        name: Annotated[str, Body(description='用户名')],
        city: Annotated[str, Body(description='城市')] = None,
        age: Annotated[int, Body(description='年龄', ge=0)] = None,
):
    data = UserService.create(name=name, city=city, age=age)
    return CreateUserResponse(data=UserInfoForCreate(**data))


@router.delete(
    path='',
    summary='删除用户',
    description='删除用户通用接口',
    response_model=OkResponse
)
def delete_user(
        user_id: Annotated[int, Body(description='用户ID', ge=0)]
):
    UserService.delete(user_id=user_id)
    return OkResponse()


@router.patch(
    path='',
    summary='更新用户',
    description='更新用户通用接口'
)
def update_user():
    return 1


@router.get(
    path='',
    summary='获取用户信息',
    description='根据用户ID获取用户信息通用接口',
    response_model=UserDetailResponse
)
def user_detail(
        user_id: Annotated[int, Query(description='用户ID', ge=0)]
):
    data = UserService.detail(user_id=user_id)
    return UserDetailResponse(data=UserInfo(**data))
