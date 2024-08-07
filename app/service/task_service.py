from app.apiserver.logger import runtime_log
from app.interface import DataBaseTransaction, KafkaConsumerManager
from app.interface.models.repo.task_repo import TaskInfoRepo, TaskRecordRepo
from app.schema.common import TaskID
from app.schema.const import KafkaTopic
from app.schema.schemas.task import (
    TaskCreateRequestBody,
    TaskDeleteRequestBody,
    TaskExecuteDataMessage,
    TaskLogExecuteDataMessage,
)
from app.service.mq_service import ChatTaskMQ, LogTaskMQ


class TaskService:

    def __init__(self):
        ...

    @staticmethod
    async def create_task(body: TaskCreateRequestBody) -> TaskID:
        async with DataBaseTransaction() as db:
            task_id = await TaskInfoRepo(db=db).create(name=body.name,
                                                       category=body.category.value,
                                                       user_id=body.user_id)
            TaskRecordRepo(db=db, task_id=task_id).create_table()
        return task_id

    @staticmethod
    async def delete_task(body: TaskDeleteRequestBody) -> None:
        async with DataBaseTransaction() as db:
            await TaskInfoRepo(db=db).delete_task(task_id=body.task_id)
            TaskRecordRepo(db=db, task_id=body.task_id).drop_table()

    @staticmethod
    async def execute_task() -> None:
        ChatTaskMQ.produce_message(name='test', age=18)
        LogTaskMQ.produce_message(num=1)

    @staticmethod
    @KafkaConsumerManager.register_consumer_func(topic=KafkaTopic.chat_task)
    def consume_task(message: TaskExecuteDataMessage):
        runtime_log.info('inside function')
        runtime_log.info(f'chat_task this is info')
        return message

    @staticmethod
    @KafkaConsumerManager.register_consumer_func(topic=KafkaTopic.log_task)
    def consume_log_task(message: TaskLogExecuteDataMessage):
        runtime_log.info('inside function')
        runtime_log.info(f'log_task this is info')
        return message
