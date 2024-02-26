from fastapi import APIRouter, Depends

from app.schema.base import BoolResponse, CommonHeaders
from app.schema.schemas.task import TaskCreateRequestBody, TaskCreateResponse, TaskDeleteRequestBody
from app.service.task_service import TaskService

router = APIRouter(tags=['任务管理模块'], dependencies=[Depends(CommonHeaders)])


@router.post(
    path='/task',
    summary='创建任务',
    description='创建任务通用接口',
    response_model=TaskCreateResponse
)
async def task_create(body: TaskCreateRequestBody):
    task_id = await TaskService().create_task(body=body)
    return TaskCreateResponse(data=task_id)


@router.delete(
    path='/task',
    summary='删除任务',
    description='删除任务通用接口',
    response_model=BoolResponse
)
async def task_create(body: TaskDeleteRequestBody):
    await TaskService().delete_task(body=body)
    return BoolResponse(data=True)


@router.get(
    path='/task/list',
    summary='任务列表',
    description='获取任务列表',
    response_model=BoolResponse
)
async def list_task(body: TaskDeleteRequestBody):
    await TaskService().delete_task(body=body)
    return BoolResponse(data=True)
