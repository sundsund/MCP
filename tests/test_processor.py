import pytest
from unittest.mock import MagicMock, patch
from mcp_project.worker.processor import DisputeProcessor
from mcp_project.common.models import StreamType

@patch('mcp_project.worker.processor.get_db_session')
def test_processor_dispatch(mock_get_db_session):
    mock_session = MagicMock()
    mock_get_db_session.return_value = mock_session

    processor = DisputeProcessor()

    # Test Eligibility
    payload = {"claim_id": "C1", "stream_type": "eligibility"}
    processor.process("P1", payload)

    assert mock_session.add.called
    assert mock_session.commit.called
    # Check if handle_eligibility was logic was applied (sub_operations added)
    # The actual object added to session
    dispute_obj = mock_session.add.call_args[0][0]
    assert "verify_coverage" in dispute_obj.data['sub_operations']

@patch('mcp_project.worker.processor.get_db_session')
def test_processor_all_streams(mock_get_db_session):
    mock_session = MagicMock()
    mock_get_db_session.return_value = mock_session
    processor = DisputeProcessor()

    for stream in StreamType:
        payload = {"claim_id": "test", "stream_type": stream.value}
        processor.process("P1", payload)
        dispute_obj = mock_session.add.call_args[0][0]
        assert dispute_obj.status.value == "completed"
        if stream == StreamType.PHARMACY_BENEFIT:
             assert "formulary_verification" in dispute_obj.data['sub_operations']
