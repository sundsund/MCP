import pytest
from unittest.mock import MagicMock, patch
import json

@patch('mcp_project.scheduler.producer.Producer')
@patch('mcp_project.worker.consumer.Consumer')
@patch('mcp_project.worker.processor.get_db_session')
def test_end_to_end_flow(mock_get_db_session, mock_consumer_class, mock_producer_class):
    # Setup Mocks
    mock_producer = MagicMock()
    mock_producer_class.return_value = mock_producer

    mock_consumer = MagicMock()
    mock_consumer_class.return_value = mock_consumer

    mock_session = MagicMock()
    mock_get_db_session.return_value = mock_session

    # 1. Scheduler produces a message
    from mcp_project.scheduler.producer import KafkaProducer
    kp = KafkaProducer()
    kp.produce_dispute("topic", "P1", {"claim_id": "C1", "stream_type": "eligibility"})

    assert mock_producer.produce.called

    # 2. Worker consumes and processes
    from mcp_project.worker.consumer import KafkaConsumer
    from mcp_project.worker.processor import DisputeProcessor

    kc = KafkaConsumer("group1")
    # Simulate a message poll
    mock_msg = MagicMock()
    mock_msg.value.return_value = json.dumps({
        "provider_id": "P1",
        "dispute": {"claim_id": "C1", "stream_type": "eligibility"}
    }).encode('utf-8')
    mock_msg.error.return_value = None
    mock_consumer.poll.return_value = mock_msg

    received_payload = kc.poll()
    assert received_payload['provider_id'] == "P1"

    processor = DisputeProcessor()
    processor.process(received_payload['provider_id'], received_payload['dispute'])

    assert mock_session.commit.called
    dispute_obj = mock_session.add.call_args[0][0]
    assert dispute_obj.status.value == "completed"
