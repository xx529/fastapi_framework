import inspect
import json
from threading import Thread
from typing import Any, Callable, Dict, Tuple

from kafka import KafkaConsumer, KafkaProducer
from loguru import logger

from app.apiserver.logger import kafka_log
from app.config import kafka_conf
from app.schema.base import KafkaMessage
from app.schema.enum import KafkaTopic


class KafkaProducerManager:
    client: KafkaProducer

    def produce(self, message: KafkaMessage):
        json_message = message.model_dump_json(indent=4)
        kafka_log.info(f'produce message \n{json_message}')
        self.client.send(message.topic.value, json_message.encode('utf-8'))

    @classmethod
    def startup(cls):
        kafka_log.info('startup kafka producer')
        cls.client = KafkaProducer(bootstrap_servers=kafka_conf.bootstrap_servers)

    @classmethod
    def shutdown(cls):
        kafka_log.info('shutdown kafka producer')
        cls.client.close()


class KafkaConsumerManager:
    consume_func: Dict[str, Tuple[Callable, Any]] = {}
    workers: Dict[str, Thread] = {}

    @staticmethod
    def consume(consumer: KafkaConsumer, func: Callable, pydantic_model):
        for msg in consumer:
            message: KafkaMessage = pydantic_model(**json.loads(msg.value.decode('utf-8')))
            with logger.contextualize(trace_id=message.trace_id):
                kafka_log.info(f'consume message '
                               f'partition: {msg.partition} '
                               f'offset: {msg.offset} '
                               f'\n{message.model_dump_json(indent=4)}')
                func(message)
                kafka_log.info('success consume message')
                consumer.commit()

    @classmethod
    def start_consumer_worker(cls, topic_name, bootstrap_servers: str, group_id: str):
        consumer = KafkaConsumer(topic_name,
                                 bootstrap_servers=bootstrap_servers,
                                 auto_offset_reset='earliest',
                                 group_id=group_id,
                                 enable_auto_commit=False)
        func, pydantic_model = cls.consume_func[topic_name]
        worker = Thread(target=cls.consume, args=(consumer, func, pydantic_model))
        worker.start()
        cls.workers[topic_name] = worker

    @classmethod
    def consumer_func(cls, topic: KafkaTopic):
        def inner(func: Callable):
            for param in inspect.signature(func).parameters.values():
                cls.consume_func[topic.value] = (func, param.annotation)
                break
            return None

        return inner

    @classmethod
    def startup(cls):
        for t in kafka_conf.topics.values():
            if t.enable is False:
                continue

            # TODO 启动多个 worker
            for num in range(1, t.num_consumers + 1):
                kafka_log.info(f'startup kafka consumer `{t.topic_name}`')
                cls.start_consumer_worker(t.topic_name, kafka_conf.bootstrap_servers, t.group_id)
                kafka_log.info(f'start worker {num} for topic: `{t.topic_name}`')

    @classmethod
    def shutdown(cls):
        ...
        # TODO: shutdown kafka consumer thread
