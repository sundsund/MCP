import os
import signal
import sys
from .consumer import KafkaConsumer
from .processor import DisputeProcessor

def main():
    topic = os.getenv('KAFKA_TOPIC', 'dispute-resolution')
    group_id = os.getenv('KAFKA_GROUP_ID', 'dispute-worker-group')

    consumer = KafkaConsumer(group_id)
    consumer.subscribe([topic])

    processor = DisputeProcessor()

    print(f"Worker started, consuming from {topic}...")

    def signal_handler(sig, frame):
        print("Stopping worker...")
        consumer.close()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        while True:
            msg_payload = consumer.poll(timeout=1.0)
            if msg_payload:
                provider_id = msg_payload.get('provider_id')
                dispute_data = msg_payload.get('dispute')
                if provider_id and dispute_data:
                    processor.process(provider_id, dispute_data)
    except Exception as e:
        print(f"Unexpected error in worker loop: {e}")
    finally:
        consumer.close()

if __name__ == "__main__":
    main()
