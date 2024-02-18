from fastapi import APIRouter, Depends

from app.schema.base import HeaderParams
from app.schema.task import TaskCreateRequestBody, TaskCreateResponse
from app.service.task_service import TaskService

router = APIRouter(tags=['任务管理模块'], dependencies=[Depends(HeaderParams.get_common_headers)])


@router.post(
    path='/task',
    summary='创建任务',
    description='创建任务通用接口',
    response_model=TaskCreateResponse
)
async def task_create(body: TaskCreateRequestBody):
    task_id = await TaskService.create_task(param=body)
    return TaskCreateResponse(data=task_id)
