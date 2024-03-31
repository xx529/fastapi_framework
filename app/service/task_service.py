from sqlalchemy.ext.asyncio import AsyncSession

from app.interface import AsyncDataBaseTransaction
from app.interface.mq.kafka import KafkaProducerClient
from app.interface.repo.task_repo import TaskInfoRepo, TaskRecordRepo
from app.schema.base import KafkaMessage, TaskID
from app.schema.enum import KafkaTopics
from app.schema.schemas.task import TaskCreateRequestBody, TaskDeleteRequestBody
from app.apiserver.logger import runtime_log


class TaskService:

    def __init__(self):
        ...

    @staticmethod
    async def create_task(body: TaskCreateRequestBody) -> TaskID:
        async with AsyncDataBaseTransaction() as db:
            task_id = await TaskInfoRepo(db=db).create(name=body.name,
                                                       category=body.category.value,
                                                       user_id=body.user_id)
            TaskRecordRepo(db=db, task_id=task_id).create_table()
        return task_id

    @staticmethod
    async def delete_task(body: TaskDeleteRequestBody) -> None:
        async with AsyncDataBaseTransaction() as db:
            await TaskInfoRepo(db=db).delete_task(task_id=body.task_id)
            TaskRecordRepo(db=db, task_id=body.task_id).drop_table()

    async def execute_task(self):
        KafkaProducerClient(topic=KafkaTopics.chat_task).produce(KafkaMessage(message={'asdf': '1234891'}))
