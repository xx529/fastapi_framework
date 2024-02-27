from typing import Annotated

from pydantic import BaseModel, Field

from app.schema.base import JsonResponse, TaskID, UserID
from app.schema.enum import TaskCategory

TaskName = Annotated[str, Field(title='任务名称', description='任务名称', example='任务1', min_length=1)]


class TaskCreateRequestBody(BaseModel):
    user_id: UserID
    name: TaskName
    category: TaskCategory


class TaskDeleteRequestBody(BaseModel):
    task_id: TaskID


class TaskCreateResponse(JsonResponse):
    data: TaskID


class TaskInfo(BaseModel):
    task_id: TaskID
    name: TaskName
    category: TaskCategory
