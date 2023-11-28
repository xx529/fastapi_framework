from fastapi import APIRouter, Query
from app.schema.user import UserListResponse, UserResponse, UserInfo
from app.service.user import UserService
from typing import Annotated

router = APIRouter(prefix='/user', tags=['user'])


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
    description='创建用户通用接口'
)
def add_user():
    return 1


@router.delete(
    path='',
    summary='删除用户',
    description='删除用户通用接口'
)
def delete_user():
    return 1


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
    response_model=UserResponse
)
def user(
        user_id: Annotated[int, Query(description='用户ID', ge=0)]
):
    data = UserService.detail(user_id=user_id)
    return UserResponse(data=UserInfo(**data))
