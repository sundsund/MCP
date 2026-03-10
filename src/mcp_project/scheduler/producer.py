import json
import os
from confluent_kafka import Producer

class KafkaProducer:
    def __init__(self):
        # If running locally without SASL for testing
        if os.getenv('KAFKA_NO_SASL'):
            conf = {'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')}
        else:
            conf = {
                'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
                'security.protocol': os.getenv('KAFKA_SECURITY_PROTOCOL', 'SASL_SSL'),
                'sasl.mechanisms': os.getenv('KAFKA_SASL_MECHANISMS', 'SCRAM-SHA-512'),
                'sasl.username': os.getenv('KAFKA_SASL_USERNAME'),
                'sasl.password': os.getenv('KAFKA_SASL_PASSWORD'),
            }

        self.producer = Producer(conf)

    def delivery_report(self, err, msg):
        if err is not None:
            print(f'Message delivery failed: {err}')
        else:
            print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

    def produce_dispute(self, topic, provider_id, dispute_data):
        message = {
            'provider_id': provider_id,
            'dispute': dispute_data
        }
        self.producer.produce(
            topic,
            key=provider_id,
            value=json.dumps(message),
            callback=self.delivery_report
        )
        self.producer.flush()

# Delay instantiation or make it optional if needed for module import tests
if __name__ != "__main__":
    # If we are being imported by something that just wants the class
    pass

# We still want a default instance but maybe it should be lazy-loaded
# or handled differently to avoid side effects during patch
producer = None
def get_producer():
    global producer
    if producer is None:
        producer = KafkaProducer()
    return producer
