from typing import Annotated

from fastapi import APIRouter, Body, Depends

from app.schema.base import BoolResponse, CommonHeaders, OkResponse, PageQueryParams
from app.schema.schemas.user import (
    UserCreateBody, UserCreateResponse, UserDeleteBody, UserDetailQuery, UserDetailResponse,
    UserListResponse, UserUpdateBody,
)
from app.service.user_service import UserService

router = APIRouter(tags=['用户管理模块'], dependencies=[Depends(CommonHeaders)])


@router.post(
    path='/user',
    summary='创建用户',
    description='创建用户通用接口',
    response_model=UserCreateResponse
)
async def user_create(
        body: Annotated[UserCreateBody, Body(openapi_examples=UserCreateBody.openapi_examples())]
):
    user_id = await UserService.create_user(name=body.name, age=body.age, gender=body.gender)
    return UserCreateResponse(data=user_id)


@router.delete(
    path='/user',
    summary='删除用户',
    description='删除用户通用接口，此接口是物理删除',
    response_model=OkResponse
)
async def user_delete(body: UserDeleteBody):
    await UserService.delete_user(user_id=body.user_id)
    return OkResponse()


@router.patch(
    path='/user',
    summary='更新用户',
    description='更新用户通用接口',
    response_model=BoolResponse
)
async def user_update(body: UserUpdateBody):
    await UserService.update_user(user_id=body.user_id, name=body.name, age=body.age, gender=body.gender)
    return BoolResponse(data=True)


@router.get(
    path='/user',
    summary='查询用户',
    description='根据用户ID获取用户信息通用接口',
    response_model=UserDetailResponse

)
async def user_detail(
        # user_id: int = Query(description='用户ID', ge=0, examples=['aaa'])
        query: UserDetailQuery = Depends()
):

    data = await UserService.detail(user_id=query.user_id)
    return UserDetailResponse(data=data)


@router.get(
    path='/user/list',
    summary='获取用户列表',
    description='获取用户列表通用接口',
    response_model=UserListResponse
)
async def user_list(query: PageQueryParams = Depends()):
    data, total = await UserService.list(page=query.page,
                                         limit=query.limit,
                                         search=query.search,
                                         order_by=query.order_by,
                                         order_type=query.order_type)

    return UserListResponse(data=data, total=total)
