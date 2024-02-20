from typing import Literal

from fastapi import APIRouter, Body, Depends, Query

from app.schema.base import BoolResponse, CommonHeaders, OkResponse
from app.schema.enum import OrderTypeEnum
from app.schema.schemas.user import UserCreateResponse, UserDetailResponse, UserListResponse
from app.service.user_service import UserService

router = APIRouter(tags=['用户管理模块'], dependencies=[Depends(CommonHeaders)])


@router.post(
    path='/user',
    summary='创建用户',
    description='创建用户通用接口',
    response_model=UserCreateResponse
)
async def user_create(
        name: str = Body(description='用户名', examples=['张三']),
        age: int = Body(description='年龄', ge=0, examples=[18]),
        gender: Literal['男', '女'] = Body(description='性别')
):
    user_id = await UserService.create_user(name=name, age=age, gender=gender)
    return UserCreateResponse(data=user_id)


@router.delete(
    path='/user',
    summary='删除用户',
    description='删除用户通用接口，此接口是物理删除',
    response_model=OkResponse
)
async def user_delete(
        user_id: int = Body(description='用户ID', ge=0)
):
    await UserService.delete_user(user_id=user_id)
    return OkResponse()


@router.patch(
    path='/user',
    summary='更新用户',
    description='更新用户通用接口',
    response_model=BoolResponse
)
async def user_update(
        user_id: int = Body(description='用户ID', ge=0, examples=[2]),
        name: str = Body(None, description='用户名', examples=['李四']),
        age: int = Body(None, description='年龄', ge=0, examples=[18]),
        gender: Literal['男', '女'] = Body(None, description='性别', examples=['男']),
):
    await UserService.update_user(user_id=user_id, name=name, age=age, gender=gender)
    return BoolResponse(data=True)


@router.get(
    path='/user',
    summary='查询用户',
    description='根据用户ID获取用户信息通用接口',
    response_model=UserDetailResponse

)
async def user_detail(
        user_id: int = Query(description='用户ID', ge=0, examples=['aaa'])
):
    data = await UserService.detail(user_id=user_id)
    return UserDetailResponse(data=data)


@router.get(
    path='/user/list',
    summary='获取用户列表',
    description='获取用户列表通用接口',
    response_model=UserListResponse
)
async def user_list(
        page: int = Query(default=1, description='页码'),
        limit: int = Query(default=10, description='每页数量'),
        order_type: OrderTypeEnum = Query(default=OrderTypeEnum.DESC.value, description='排序方式'),
        order_by: str = Query(default='create_at', description='排序字段'),
        search: str = Query(default=None, description='搜索关键字', example='张三'),
):
    data, total = await UserService.list(page=page,
                                         limit=limit,
                                         search=search,
                                         order_by=order_by,
                                         order_type=order_type)

    return UserListResponse(data=data, total=total)
