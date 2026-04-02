"""Certification and badge authority."""
from sqlalchemy import Column, String, JSON, ForeignKey, Boolean, DateTime, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
import uuid
from datetime import datetime, timedelta
from .base import TimestampedModel


class Certification(TimestampedModel):
    """Issued certification badge."""
    __tablename__ = "certifications"
    
    certification_id = Column(String(100), unique=True, nullable=False, index=True)
    model_id = Column(UUID(as_uuid=True), ForeignKey("ai_models.id"), nullable=False)
    audit_id = Column(UUID(as_uuid=True), ForeignKey("audits.id"), nullable=False)
    score_id = Column(UUID(as_uuid=True), ForeignKey("scores.id"), nullable=False)
    
    # Certification details
    certification_tier = Column(String(50), nullable=False)  # Experimental, Controlled, Production, Enterprise
    ai_trust_score = Column(Float, nullable=False)
    
    # Temporal
    issued_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False)  # Default 12 months
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    is_revoked = Column(Boolean, default=False, index=True)
    revocation_reason = Column(String(512))
    revocation_timestamp = Column(DateTime)
    
    # Public verification
    verification_url = Column(String(512))
    verification_hash = Column(String(512))  # Tamper detection
    
    # Compliance metadata
    compliance_mappings = Column(JSONB)  # EU AI Act, NIST, OECD, ISO references
    liability_disclaimer = Column(Text)
    
    # Certificate rendering
    certificate_svg = Column(Text)  # Rendered certificate
    certificate_pdf_url = Column(String(512))
    qr_code_data = Column(String(512))
    
    def __repr__(self):
        return f"<Certification {self.certification_id} Tier={self.certification_tier}>"
