from typing import List

from fastapi import APIRouter, Body, Depends, File, UploadFile

from app.schema.base import BoolResponse, CommonHeaders
from app.schema.schemas.task import TaskCreateRequestBody, TaskCreateResponse, TaskDeleteRequestBody
from app.service.task_service import TaskService

router = APIRouter(tags=['任务管理模块'], dependencies=[Depends(CommonHeaders)])


@router.post(
    path='/task',
    summary='创建任务',
    description='创建任务通用接口',
    response_model=TaskCreateResponse,
    response_description='返回任务ID'
)
async def task_create(body: TaskCreateRequestBody):
    task_id = await TaskService().create_task(body=body)
    return TaskCreateResponse(data=task_id)


@router.delete(
    path='/task',
    summary='删除任务',
    description='删除任务通用接口',
    response_model=BoolResponse,
    response_description='返回删除状态'
)
async def task_create(body: TaskDeleteRequestBody):
    await TaskService().delete_task(body=body)
    return BoolResponse(data=True)


@router.post(
    path='/task/upload',
    summary='数据上传',
    description='数据上传通用接口',
    response_model=BoolResponse,
    response_description='返回数据上传状态'
)
async def task_upload(
        task_id: int = Body(),
        meta_file: UploadFile = File(),
        data_files: List[UploadFile] = File(),
):
    print(task_id)
    print(meta_file.filename)
    print(data_files[0].filename)
    return BoolResponse(data=True)
