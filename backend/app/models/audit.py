"""Audit execution and test results."""
from sqlalchemy import Column, String, JSON, ForeignKey, Integer, Float, Boolean, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID, ARRAY
import uuid
from .base import TimestampedModel


class Audit(TimestampedModel):
    """Audit execution record."""
    __tablename__ = "audits"
    
    model_id = Column(UUID(as_uuid=True), ForeignKey("ai_models.id"), index=True, nullable=False)
    audit_name = Column(String(256), nullable=False)
    status = Column(String(50), default="in_progress")  # in_progress, completed, failed
    
    # Audit configuration
    test_suite_version = Column(String(50), default="1.0")
    temperature = Column(Float, default=0.0)
    
    # Results summary
    total_tests = Column(Integer, default=0)
    passed_tests = Column(Integer, default=0)
    failed_tests = Column(Integer, default=0)
    
    # Execution metadata
    started_at = Column(String)
    completed_at = Column(String)
    total_duration_ms = Column(Float)
    total_tokens_input = Column(Integer, default=0)
    total_tokens_output = Column(Integer, default=0)
    
    # Raw results
    test_results = Column(JSONB)  # List of individual test results
    
    # Judge model output
    judge_assessment = Column(JSONB)  # Judge model classification
    
    # Computed scores
    is_scored = Column(Boolean, default=False)
    score_id = Column(UUID(as_uuid=True), ForeignKey("scores.id"))
    
    def __repr__(self):
        return f"<Audit {self.audit_name} Status={self.status}>"


class AuditTest(TimestampedModel):
    """Individual governance test result."""
    __tablename__ = "audit_tests"
    
    audit_id = Column(UUID(as_uuid=True), ForeignKey("audits.id"), index=True, nullable=False)
    
    # Test definition
    test_category = Column(String(100), nullable=False, index=True)
    test_name = Column(String(256), nullable=False)
    test_prompt = Column(Text, nullable=False)
    
    # Test execution
    model_response = Column(Text)
    response_tokens = Column(Integer)
    response_latency_ms = Column(Float)
    
    # Classification
    classification = Column(String(50))  # pass, fail, partial
    severity = Column(String(50))  # critical, high, medium, low
    
    # Detailed analysis
    judge_classification = Column(JSONB)  # Judge model output
    metrics = Column(JSONB)  # Test-specific metrics
    
    def __repr__(self):
        return f"<AuditTest {self.test_name} ({self.test_category})>"
