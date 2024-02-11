from typing import Annotated

from pydantic import BaseModel, Field

from app.schema.base import JsonResponse
from app.schema.enum import TaskCategory

TaskID = Annotated[int, Field(description='任务ID', example=1)]
TaskName = Annotated[str, Field(description='任务名称', example='任务1')]


class TaskCreateResponse(JsonResponse):
    data: TaskID


class TaskInfo(BaseModel):
    task_id: TaskID
    name: TaskName
    category: TaskCategory
