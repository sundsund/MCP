import pytest
from mcp_project.common.models import Dispute, StreamType, DisputeStatus

def test_stream_type_enum():
    assert StreamType.ELIGIBILITY.value == "eligibility"
    assert StreamType.COORDINATION_OF_BENEFITS.value == "coordination_of_benefits"
    assert len(StreamType) == 7

def test_dispute_model_creation():
    dispute = Dispute(
        provider_id="prov_1",
        claim_id="claim_1",
        stream_type=StreamType.ELIGIBILITY,
        status=DisputeStatus.PENDING,
        data={"test": "data"}
    )
    assert dispute.provider_id == "prov_1"
    assert dispute.status == DisputeStatus.PENDING
