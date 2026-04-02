"""AI Model registration and management."""
from sqlalchemy import Column, String, Enum, JSON, Boolean, Float
from sqlalchemy.dialects.postgresql import JSONB, UUID
import uuid
import enum
from .base import TimestampedModel


class ProviderType(str, enum.Enum):
    """Supported AI model providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    HUGGINGFACE = "huggingface"
    REPLICATE = "replicate"
    CUSTOM_HTTP = "custom_http"
    SELF_HOSTED = "self_hosted"


class AIModel(TimestampedModel):
    """Registered AI model entity."""
    __tablename__ = "ai_models"
    
    provider_type = Column(Enum(ProviderType), nullable=False, index=True)
    model_identifier = Column(String(512), nullable=False)  # e.g., "gpt-4", "claude-3"
    display_name = Column(String(256), nullable=False)
    description = Column(String(1024))
    
    # Connection details
    api_endpoint = Column(String(2048))  # For custom/self-hosted
    credential_id = Column(UUID(as_uuid=True))  # Reference to EncryptedCredential
    
    # Capabilities & configuration
    supports_temperature = Column(Boolean, default=True)
    max_tokens = Column(Float)
    context_window = Column(Float)
    
    # Status tracking
    is_active = Column(Boolean, default=True, index=True)
    is_verified = Column(Boolean, default=False)
    verification_timestamp = Column(String)
    verification_status = Column(String)  # "verified", "failed", "pending"
    
    # Metadata
    metadata = Column(JSONB)  # Provider-specific metadata
    last_audit_date = Column(String)
    audit_count = Column(Float, default=0)
    
    def __repr__(self):
        return f"<AIModel {self.display_name} ({self.provider_type})>"
