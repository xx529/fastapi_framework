import uuid
from typing import Dict

from kafka import KafkaConsumer, KafkaProducer
from loguru import logger

from app.apiserver.logger import kafka_log
from app.config import kafka_conf
from app.schema.base import KafkaMessage
from app.schema.enum import KafkaTopics


class KafkaProducerClient:
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


class KafkaConsumerClient:
    clients: Dict[str, KafkaConsumer] = {}

    def __init__(self, topic: KafkaTopics):
        self.client = self.clients[topic.value]

    def consume(self):
        with logger.contextualize(trace_id=uuid.uuid4().hex):
            ...

    @classmethod
    def startup(cls):
        enable_topics = [t for t in kafka_conf.topics.values() if t.enable is True]
        for t in enable_topics:
            kafka_log.info(f'startup kafka consumer `{t.topic_name}`')
            cls.clients[t.topic_name] = KafkaConsumer(t.topic_name,
                                                      bootstrap_servers=kafka_conf.bootstrap_servers,
                                                      enable_auto_commit=False)

    @classmethod
    def shutdown(cls):
        for topic_name, consumer in cls.clients.items():
            kafka_log.info(f'shutdown kafka consumer `{topic_name}`')
            consumer.close()
