from fastapi import APIRouter, Body, Depends

from app.schema.base import HeaderParams
from app.schema.enum import TaskCategory
from app.schema.task import TaskCreateResponse
from app.service.task_service import TaskService

router = APIRouter(tags=['任务管理模块'], dependencies=[Depends(HeaderParams.get_common_headers)])


@router.post(
    path='/task',
    summary='创建任务',
    description='创建任务通用接口',
    response_model=TaskCreateResponse
)
async def task_create(
        name: str = Body(description='任务名称', examples=['任务1']),
        category: TaskCategory = Body(description='任务分类', examples=[TaskCategory.NORMAL.value]),
        user_id: int = Body(description='创建的用户ID', ge=0, examples=[1])
):
    task_id = await TaskService.create_task(name=name, category=category.value, user_id=user_id)
    return TaskCreateResponse(data=task_id)
