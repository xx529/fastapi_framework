from fastapi import APIRouter, Body, Depends, Query

from app.schema.base import BoolResponse, HeaderParams, OkResponse, OrderTypeEnum
from app.schema.user import UserCreateResponse, UserDetailResponse, UserInfo, UserListResponse
from app.service.user_service import UserService

router = APIRouter(tags=['用户管理模块'], dependencies=[Depends(HeaderParams.get_common_headers)])


@router.post(
    path='/user',
    summary='创建用户',
    description='创建用户通用接口',
    response_model=UserCreateResponse
)
def user_add(
        name: str = Body(description="用户名", examples=["张三"]),
        age: int = Body(default=None, description="年龄", ge=0, examples=[18]),
):
    user_id = UserService.create(name=name, age=age)
    return UserCreateResponse(data=user_id)


@router.delete(
    path='/user',
    summary='删除用户',
    description='删除用户通用接口，此接口是物理删除',
    response_model=OkResponse
)
def user_delete(
        user_id: int = Body(description='用户ID', ge=0)
):
    UserService.delete(user_id=user_id)
    return OkResponse()


@router.patch(
    path='/user',
    summary='更新用户',
    description='更新用户通用接口',
    response_model=BoolResponse
)
def user_update(
        user_id: int = Body(description='用户ID', ge=0),
        name: str = Body(description='用户名'),
        city: str = Body(description='城市'),
        age: int = Body(description='年龄', ge=0),
):
    UserService.update(user_id=user_id, name=name, city=city, age=age)
    return BoolResponse(data=True)


@router.get(
    path='/user',
    summary='查询用户',
    description='根据用户ID获取用户信息通用接口',
    response_model=UserDetailResponse
)
def user_detail(
        user_id: int = Query(description='用户ID', ge=0, examples=["aaa"])
):
    data = UserService.detail(user_id=user_id)
    return UserDetailResponse(data=UserInfo(**data))


@router.get(
    path='/user/list',
    summary='获取用户列表',
    description='获取用户列表通用接口',
    response_model=UserListResponse
)
def user_list(
        page: int = Query(default=1, description="页码"),
        limit: int = Query(default=10, description="每页数量"),
        order_type: OrderTypeEnum = Query(default='desc', description="排序方式"),
        order_by: str = Query(default='create_at', description="排序字段"),
        search: str = Query(default=None, description="搜索关键字", example='张三'),
):
    data, total = UserService.list(page=page, limit=limit, search=search, order_by=order_by, order_type=order_type)
    return UserListResponse(data=data, total=total)
