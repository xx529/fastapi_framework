from app.apiserver.logger import runtime_log
from app.interface import AsyncDataBaseTransaction
from app.interface import KafkaConsumerManager, KafkaProducerManager
from app.interface.repo.task_repo import TaskInfoRepo, TaskRecordRepo
from app.schema.base import TaskID
from app.schema.enum import KafkaTopic
from app.schema.schemas.task import TaskCreateRequestBody, TaskDeleteRequestBody, TaskExecuteDataMessage


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
        message = TaskExecuteDataMessage(message={'name': 'test', 'age': '18'},
                                         topic=KafkaTopic.chat_task)
        KafkaProducerManager().produce(message)
        return message

    @staticmethod
    @KafkaConsumerManager.register_consumer_func(topic=KafkaTopic.chat_task)
    def consume_task(message: TaskExecuteDataMessage):
        runtime_log.info('inside function')
        runtime_log.info(f'this is info')
        return message
