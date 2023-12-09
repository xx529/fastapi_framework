from fastapi import APIRouter, Query, Body, Header, Depends
from app.schema.user import (
    UserListResponse,
    UserDetailResponse,
    UserInfo,
    CreateUserResponse,
    UserInfoForCreate,
)
from app.schema.base import OkResponse, Headers
from app.service.user_service import UserService
from typing import Annotated


def common_headers(
        authorization: str = Header(description="用户认证信息", example="kdshfkasdhfasd-asdhjflasd"),
):
    return {"Authorization": authorization}


router = APIRouter(prefix='/user', tags=['用户管理模块'])


@router.get(
    path='/list',
    summary='获取用户列表',
    description='获取用户列表通用接口',
    response_model=UserListResponse
)
def user_list(
        page: int = Query(default=1, description='页码', ge=1),
        limit: int = Query(default=10, description='每页数量', ge=1)
):
    data = UserService.list(page=page, limit=limit)
    return UserListResponse(data=data)


@router.get(
    path='',
    summary='用户信息',
    description='根据用户ID获取用户信息通用接口',
    response_model=UserDetailResponse
)
def user_detail(
        user_id: int = Query(description='用户ID', ge=0)
):
    # print(headers.task)
    data = UserService.detail(user_id=user_id)
    return UserDetailResponse(data=UserInfo(**data))


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


@router.patch(
    path='',
    summary='更新用户',
    description='更新用户通用接口',
    response_model=OkResponse
)
def update_user(
        user_id: Annotated[int, Body(description='用户ID', ge=0)],
        name: Annotated[str, Body(description='用户名')],
        city: Annotated[str, Body(description='城市')],
        age: Annotated[int, Body(description='年龄', ge=0)],
):
    UserService.update(user_id=user_id, name=name, city=city, age=age)
    return OkResponse()


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
