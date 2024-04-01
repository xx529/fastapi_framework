from app.interface import AsyncDataBaseTransaction
from app.interface import KafkaProducerManager, KafkaConsumerManager
from app.interface.repo.task_repo import TaskInfoRepo, TaskRecordRepo
from app.schema.base import TaskID
from app.schema.enum import KafkaTopics
from app.schema.schemas.task import TaskCreateRequestBody, TaskDeleteRequestBody, TaskExecuteDataMessage
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

    @staticmethod
    async def execute_task() -> TaskExecuteDataMessage:
        message = TaskExecuteDataMessage(message={'name': 'test', 'age': '18'})
        KafkaProducerManager(topic=KafkaTopics.chat_task).produce(message)
        return message

    @staticmethod
    @KafkaConsumerManager.topic_consumer(topic=KafkaTopics.chat_task)
    def consume_task(message: TaskExecuteDataMessage):
        runtime_log.info(message.model_dump_json(indent=4))
        return message
