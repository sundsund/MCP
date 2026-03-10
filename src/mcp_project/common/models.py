from sqlalchemy import Column, Integer, String, DateTime, JSON, Enum
import enum
from datetime import datetime
from .database import Base

class StreamType(enum.Enum):
    ELIGIBILITY = "eligibility"
    MEDICAL_NECESSITY = "medical_necessity"
    BILLING_CODING = "billing_coding"
    AUTHORIZATION = "authorization"
    PHARMACY_BENEFIT = "pharmacy_benefit"
    CONTRACTUAL_DISPUTE = "contractual_dispute"
    COORDINATION_OF_BENEFITS = "coordination_of_benefits"

class DisputeStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class Dispute(Base):
    __tablename__ = "disputes"

    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(String, index=True)
    claim_id = Column(String, index=True)
    stream_type = Column(Enum(StreamType))
    status = Column(Enum(DisputeStatus), default=DisputeStatus.PENDING)
    data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Dispute(id={self.id}, stream_type={self.stream_type}, status={self.status})>"
