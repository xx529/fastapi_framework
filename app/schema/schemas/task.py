from pydantic import BaseModel

from app.schema.base import JsonResponse, TaskID, TaskName, UserID
from app.schema.enum import TaskCategory


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
