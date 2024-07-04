from fastapi import APIRouter, Body, Depends

from app.schema.request.base import CommonHeaders, PageQueryParams, WithAuthHeaders
from app.schema.response.base import BoolResponse, OkResponse
from app.schema.schemas.user import (
    UserCreateBody, UserCreateResponse, UserDeleteBody, UserDetailParam, UserDetailResponse,
    UserListResponse, UserUpdateBody,
)
from app.service.user_service import UserService
from app.utils.example import user_create_examples

router = APIRouter(tags=['用户管理模块'], dependencies=[Depends(CommonHeaders.get_from_header)])


@router.post(
    path='/user',
    summary='创建用户',
    description='创建用户通用接口',
)
async def user_create(
        headers: WithAuthHeaders = Depends(WithAuthHeaders.get_from_header),
        body: UserCreateBody = Body(openapi_examples=user_create_examples)
) -> UserCreateResponse:
    user_id = await UserService.create_user(name=body.name, age=body.age, gender=body.gender)
    print(headers)
    return UserCreateResponse(data=user_id)


@router.delete(
    path='/user',
    summary='删除用户',
    description='删除用户通用接口，此接口是物理删除',
)
async def user_delete(body: UserDeleteBody) -> OkResponse:
    await UserService.delete_user(user_id=body.user_id)
    return OkResponse()


@router.patch(
    path='/user',
    summary='更新用户',
    description='更新用户通用接口',
)
async def user_update(body: UserUpdateBody) -> BoolResponse:
    await UserService.update_user(user_id=body.user_id, name=body.name, age=body.age, gender=body.gender)
    return BoolResponse(data=True)


@router.get(
    path='/user',
    summary='查询用户',
    description='根据用户ID获取用户信息通用接口',
)
async def user_detail(param: UserDetailParam = Depends()) -> UserDetailResponse:
    data = await UserService.detail(user_id=param.user_id)
    return UserDetailResponse(data=data)


@router.get(
    path='/user/list',
    summary='获取用户列表',
    description='获取用户列表通用接口',
)
async def user_list(param: PageQueryParams = Depends()) -> UserListResponse:
    data, total = await UserService.list(page=param.page,
                                         limit=param.limit,
                                         search=param.search,
                                         order_by=param.order_by,
                                         order_type=param.order_type)

    return UserListResponse(data=data, total=total)
