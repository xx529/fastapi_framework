import inspect
from typing import Any, Callable, Dict, Tuple

from kafka import KafkaConsumer, KafkaProducer
from loguru import logger

from app.apiserver.logger import kafka_log
from app.config import kafka_conf
from app.schema.base import KafkaMessage
from app.schema.enum import KafkaTopics


class KafkaProducerManager:
    client: KafkaProducer

    def __init__(self, topic: KafkaTopics):
        self.topic = topic.value

    def produce(self, message: KafkaMessage):
        json_message = message.model_dump_json(indent=4)
        kafka_log.info(f'produce message to `{self.topic}`: \n{json_message}')
        self.client.send(self.topic, json_message.encode('utf-8'))

    @classmethod
    def startup(cls):
        kafka_log.info('startup kafka producer')
        cls.client = KafkaProducer(bootstrap_servers=kafka_conf.bootstrap_servers)

    @classmethod
    def shutdown(cls):
        kafka_log.info('shutdown kafka producer')
        cls.client.close()


class KafkaConsumerManager:
    clients: Dict[str, KafkaConsumer] = {}
    consume_func: Dict[str, Tuple[Callable, Any]] = {}

    def __init__(self, topic: KafkaTopics):
        self.client = self.clients[topic.value]

    @staticmethod
    def consume(topic: KafkaTopics, consumer: KafkaConsumer, func: Callable, pydantic_model):
        for _message in consumer:
            message: KafkaMessage = pydantic_model(**_message.value.decode('utf-8'))
            with logger.contextualize(trace_id=message.trace_id):
                kafka_log.info(f'consume topic: {topic.value} for message: \n{message.model_dump_json(indent=4)}')
                func(message)
                kafka_log.info('success consumer message')
                consumer.commit()

    @classmethod
    def topic_consumer(cls, topic: KafkaTopics):
        def inner(func: Callable):
            for param in inspect.signature(func).parameters.values():
                cls.consume_func[topic.value] = (func, param.annotation)
                break

            return None

        return inner

    @classmethod
    def startup(cls):
        for t in kafka_conf.topics.values():
            if t.enable is True:
                kafka_log.info(f'startup kafka consumer `{t.topic_name}`')
                cls.clients[t.topic_name] = KafkaConsumer(t.topic_name,
                                                          bootstrap_servers=kafka_conf.bootstrap_servers,
                                                          auto_offset_reset='earliest',
                                                          group_id=t.group_id,
                                                          enable_auto_commit=False)

                kafka_log.info(f'binding `{cls.consume_func[t.topic_name][0]}`; '
                               f'param class {cls.consume_func[t.topic_name][1]}; '
                               f'to `{t.topic_name}`')

    @classmethod
    def shutdown(cls):
        for topic_name, consumer in cls.clients.items():
            kafka_log.info(f'shutdown kafka consumer `{topic_name}`')
            consumer.close()
