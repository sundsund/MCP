import json
import os
from confluent_kafka import Consumer, KafkaError

class KafkaConsumer:
    def __init__(self, group_id):
        conf = {
            'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
            'group.id': group_id,
            'auto.offset.reset': 'earliest',
            'security.protocol': os.getenv('KAFKA_SECURITY_PROTOCOL', 'SASL_SSL'),
            'sasl.mechanisms': os.getenv('KAFKA_SASL_MECHANISMS', 'SCRAM-SHA-512'),
            'sasl.username': os.getenv('KAFKA_SASL_USERNAME'),
            'sasl.password': os.getenv('KAFKA_SASL_PASSWORD'),
        }

        if os.getenv('KAFKA_NO_SASL'):
            conf = {
                'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
                'group.id': group_id,
                'auto.offset.reset': 'earliest'
            }

        self.consumer = Consumer(conf)

    def subscribe(self, topics):
        self.consumer.subscribe(topics)

    def poll(self, timeout=1.0):
        msg = self.consumer.poll(timeout)
        if msg is None:
            return None
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                return None
            else:
                print(f"Consumer error: {msg.error()}")
                return None

        return json.loads(msg.value().decode('utf-8'))

    def close(self):
        self.consumer.close()
