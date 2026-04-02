"""Immutable audit logging."""
from sqlalchemy import Column, String, Text, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, UUID
import uuid
from .base import TimestampedModel


class AuditLog(TimestampedModel):
    """Immutable execution and security log."""
    __tablename__ = "audit_logs"
    
    # Reference
    audit_id = Column(UUID(as_uuid=True), ForeignKey("audits.id"))
    model_id = Column(UUID(as_uuid=True), ForeignKey("ai_models.id"))
    
    # Log entry
    log_level = Column(String(50))  # INFO, WARN, ERROR, CRITICAL
    log_category = Column(String(100))  # test_execution, credential_access, score_calculation
    message = Column(Text)
    
    # Trace data
    trace_data = Column(JSONB)  # Full context
    
    # Security
    user_id = Column(String(256))
    session_id = Column(String(256))
    ip_address = Column(String(50))
    
    # Integrity
    hash_chain = Column(String(512))  # Link to previous log for immutability
    signature = Column(String(512))
    
    def __repr__(self):
        return f"<AuditLog {self.log_level} - {self.log_category}>"
