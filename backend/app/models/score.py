"""AI Trust Score and dimension scoring."""
from sqlalchemy import Column, String, JSON, ForeignKey, Float, Boolean, Integer
from sqlalchemy.dialects.postgresql import JSONB, UUID
import uuid
from .base import TimestampedModel


class Score(TimestampedModel):
    """RATIO AI Trust Score."""
    __tablename__ = "scores"
    
    audit_id = Column(UUID(as_uuid=True), ForeignKey("audits.id"), unique=True, nullable=False)
    
    # AI TRUST SCORE (0-900)
    ai_trust_score = Column(Float, nullable=False)
    
    # Dimension scores (0-100)
    governance_score = Column(Float)
    security_score = Column(Float)
    reliability_score = Column(Float)
    fairness_score = Column(Float)
    behavior_score = Column(Float)
    transparency_score = Column(Float)
    
    # Dimension weights and normalized contributions
    dimension_breakdown = Column(JSONB)  # Detailed per-dimension metrics
    
    # Risk assessment
    risk_tier = Column(String(50))  # Low, Medium, High
    eligibility_level = Column(String(50))  # Experimental, Controlled, Production, Enterprise
    
    # Metrics raw data
    metrics = Column(JSONB)  # All raw metrics that fed into scoring
    
    # Scoring metadata
    scoring_version = Column(String(50), default="1.0")
    calculation_timestamp = Column(String)
    human_review_required = Column(Boolean, default=False)
    human_review_reason = Column(String(512))
    
    # Improvement recommendations
    recommendations = Column(JSONB)  # Rule-based improvement actions
    
    def __repr__(self):
        return f"<Score AI_TRUST={self.ai_trust_score} Tier={self.risk_tier}>"
