import inspect
import json
import traceback
from threading import Thread
from typing import Any, Callable, Dict, Tuple

from kafka import KafkaConsumer, KafkaProducer
from loguru import logger

from app.apiserver.logger import kafka_log
from app.config import kafka_conf
from app.schema.base import KafkaMessage
from app.schema.enum import KafkaTopic


class KafkaProducerManager:
    client: KafkaProducer = None

    @classmethod
    def produce(cls, message: KafkaMessage):
        json_message = message.model_dump_json(indent=4)
        kafka_log.info(f'produce message \n{json_message}')
        cls.client.send(message.topic.value, json_message.encode('utf-8'))

    @classmethod
    def startup(cls):
        kafka_log.info('startup kafka producer')
        cls.client = KafkaProducer(bootstrap_servers=kafka_conf.bootstrap_servers)

    @classmethod
    def shutdown(cls):
        if cls.client is not None:
            kafka_log.info('shutdown kafka producer')
            cls.client.close()


class KafkaConsumerManager:
    consume_func: Dict[str, Tuple[Callable, Any]] = {}
    workers: Dict[str, "ConsumerWorker"] = {}

    @classmethod
    def start_consumer_worker(cls, topic_name, bootstrap_servers: str, group_id: str, worker_number: int):
        worker_func, pydantic_model = cls.consume_func[topic_name]
        worker_name = f'{topic_name}_{worker_number}'
        worker = ConsumerWorker(worker_name=worker_name,
                                pydantic_model=pydantic_model,
                                worker_func=worker_func,
                                topic_name=topic_name,
                                bootstrap_servers=bootstrap_servers,
                                group_id=group_id)
        worker.start()
        cls.workers[worker_name] = worker
        kafka_log.info(f'start worker `{worker_name}`')

    @classmethod
    def register_consumer_func(cls, topic: KafkaTopic):
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

            kafka_log.info(f'startup kafka consumer for topic `{t.topic_name}`')
            for num in range(1, t.num_consumers + 1):
                cls.start_consumer_worker(topic_name=t.topic_name,
                                          bootstrap_servers=kafka_conf.bootstrap_servers,
                                          group_id=t.group_id,
                                          worker_number=num)

    @classmethod
    def shutdown(cls):
        kafka_log.info('shutdown kafka consumers')
        for worker_name, worker in cls.workers.items():
            kafka_log.info(f'shutdown worker `{worker_name}`')
            worker.stop()
            worker.join()


class ConsumerWorker(Thread):
    def __init__(self,
                 worker_name: str,
                 topic_name: str,
                 bootstrap_servers: str,
                 group_id: str,
                 worker_func: Callable,
                 pydantic_model):

        Thread.__init__(self)
        self.worker_name = worker_name
        self.worker_func = worker_func
        self.pydantic_model = pydantic_model
        self.topic_name = topic_name
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.running = True

    def run(self):

        # 创建kafka消费者
        consumer = KafkaConsumer(self.topic_name,
                                 bootstrap_servers=self.bootstrap_servers,
                                 auto_offset_reset='earliest',
                                 group_id=self.group_id,
                                 enable_auto_commit=False)

        while True:
            records = consumer.poll(timeout_ms=1000)

            for _, messages in records.items():
                for msg in messages:
                    # 还原函数的参数
                    message: KafkaMessage = self.pydantic_model(**json.loads(msg.value.decode('utf-8')))

                    # 以 trace_id 为跟踪上下文
                    with logger.contextualize(trace_id=f'{message.trace_id}-{self.worker_name}'):
                        LoggerStep.reset_step_num()
                        kafka_log.info(f'consume message '
                                       f'partition: {msg.partition} '
                                       f'offset: {msg.offset} '
                                       f'by worker `{self.worker_name}` '
                                       f'\n{message.model_dump_json(indent=4)}')
                        # 处理消息
                        self.consume_message(message)

                        # 提交偏移量
                        consumer.commit()

            # 如果要关闭线程，则关闭消费者，并跳出循环
            if self.running is False:
                consumer.close()
                break

    def consume_message(self, message: KafkaMessage):
        try:
            self.worker_func(message)
            kafka_log.info('finish consume message')
        except Exception as e:
            kafka_log.error(str(e))
            kafka_log.error(traceback.format_exc())

    def stop(self):
        self.running = False
