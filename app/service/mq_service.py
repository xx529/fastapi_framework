from abc import abstractmethod

from app.interface import KafkaProducerManager
from app.schema.base import KafkaMessage
from app.schema.const import KafkaTopic
from app.schema.schemas.task import (
    TaskExecuteDataMessage, TaskExecuteInfo, TaskLogExecuteDataMessage,
    TaskLogExecuteInfo,
)

kafka_producer = KafkaProducerManager()


class BaseMQ:
    topic: KafkaTopic
    producer: KafkaProducerManager = kafka_producer

    @abstractmethod
    def produce_message(self, *args, **kwargs) -> KafkaMessage:
        ...

    # @abstractmethod
    # def consume_message(self, *args, **kwargs):
    #     ...


class ChatTaskMQ(BaseMQ):
    topic = KafkaTopic.chat_task

    @classmethod
    def produce_message(cls, name: str, age: int) -> TaskExecuteDataMessage:
        data = TaskExecuteInfo(name=name, age=age)
        message = TaskExecuteDataMessage(data=data, topic=cls.topic)
        cls.producer.produce(message)
        return message

    def consume_message(self, *args, **kwargs):
        pass


class LogTaskMQ(BaseMQ):
    topic = KafkaTopic.log_task

    @classmethod
    def produce_message(cls, num: int) -> TaskLogExecuteDataMessage:
        data = TaskLogExecuteInfo(num=num)
        message = TaskLogExecuteDataMessage(data=data, topic=cls.topic)
        cls.producer.produce(message)
        return message

    def consume_message(self, *args, **kwargs):
        pass
