import os
from apscheduler.schedulers.blocking import BlockingScheduler
from .producer import get_producer
from ..common.models import StreamType
import time

def schedule_dispute_check():
    print("Checking for new disputes to process...")
    # Simulation logic
    providers = os.getenv('SIMULATED_PROVIDERS', 'provider_a,provider_b').split(',')

    producer = get_producer()
    for provider_id in providers:
        provider_id = provider_id.strip()
        for stream in StreamType:
            dispute_data = {
                "claim_id": f"CLAIM-{int(time.time())}",
                "stream_type": stream.value,
                "details": f"Sample dispute for {stream.value}"
            }
            print(f"Scheduling dispute for {provider_id} - {stream.value}")
            producer.produce_dispute(
                topic=os.getenv('KAFKA_TOPIC', 'dispute-resolution'),
                provider_id=provider_id,
                dispute_data=dispute_data
            )

def main():
    scheduler = BlockingScheduler()
    interval = int(os.getenv('SCHEDULER_INTERVAL_MINUTES', '1'))

    scheduler.add_job(schedule_dispute_check, 'interval', minutes=interval)

    print(f"Scheduler started (interval: {interval} min). Press Ctrl+C to exit.")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == "__main__":
    main()
