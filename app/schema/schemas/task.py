from typing import List

from fastapi import Form, UploadFile
from pydantic import BaseModel, Field

from app.schema.base import JsonResponse, KafkaMessage, TaskID, UserID
from app.schema.const import TaskCategory


class TaskCreateRequestBody(BaseModel):
    user_id: UserID = Field(title='用户ID', description='用户ID', examples=[1])
    name: str = Field(title='任务名称', description='任务名称', examples=['任务1'], min_length=1)
    category: TaskCategory = Field(title='任务分类', description='任务分类', examples=[TaskCategory.NORMAL.value])


class TaskDeleteRequestBody(BaseModel):
    task_id: TaskID = Field(title='任务ID', description='任务ID', example=1)


class TaskCreateResponse(JsonResponse):
    data: TaskID = Field(title='任务ID', description='任务ID', example=1)


class TaskInfo(BaseModel):
    task_id: TaskID = Field(title='任务ID', description='任务ID', example=1)
    name: str = Field(title='任务名称', description='任务名称', examples=['任务1'], min_length=1)
    category: TaskCategory


class TaskExecuteInfo(BaseModel):
    name: str
    age: int


class TaskLogExecuteInfo(BaseModel):
    num: int


class TaskExecuteDataMessage(KafkaMessage):
    data: TaskExecuteInfo


class TaskLogExecuteDataMessage(KafkaMessage):
    data: TaskLogExecuteInfo


class Test(BaseModel):
    name: str
    value: int


class TaskUploadBody(BaseModel):
    # test: Test = Field(title='测试', description='测试')
    task_id: int = Field(title='任务ID', description='任务ID')
    meta_file: UploadFile = Field(title='描述文件', description='描述文件')
    data_files: List[UploadFile] = Field(title='数据文件', description='数据文件')

    @staticmethod
    def from_form_body(
            task_id: int = Form(media_type='multipart/form-data', title='任务ID', description='任务ID'),
            meta_file: UploadFile = Form(title='描述文件', description='描述文件', media_type='multipart/form-data'),
            data_files: List[UploadFile] = Form(title='数据文件', description='数据文件',
                                                media_type='multipart/form-data')
    ):
        return TaskUploadBody(meta_file=meta_file, data_files=data_files, task_id=task_id)
