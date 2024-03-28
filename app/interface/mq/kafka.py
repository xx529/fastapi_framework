from kafka import KafkaConsumer, KafkaProducer

from app.apiserver.logger import kafka_log


class KafkaProducerClient:
    client: KafkaProducer

    def __init__(self, topic):
        self.topic = topic

    def produce(self, message):
        self.client.send(self.topic, message)

    @classmethod
    def startup(cls):
        kafka_log.info('startup kafka producer')
        cls.client = KafkaProducer(bootstrap_servers='localhost:9092')


class KafkaConsumerClient:
    client: KafkaConsumer

    @classmethod
    def startup(cls):
        topics = ['topic1', 'topic2']
        kafka_log.info(f'startup kafka consumer {topics}')
        cls.client = KafkaConsumer(*topics, bootstrap_servers='localhost:9092')
