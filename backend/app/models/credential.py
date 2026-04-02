"""Encrypted credential storage."""
from sqlalchemy import Column, String, Boolean, LargeBinary
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .base import TimestampedModel


class EncryptedCredential(TimestampedModel):
    """Encrypted API credentials for model connectors."""
    __tablename__ = "encrypted_credentials"
    
    provider_type = Column(String(50), nullable=False)
    credential_name = Column(String(256), nullable=False)
    
    # Encrypted storage
    encrypted_key = Column(LargeBinary, nullable=False)
    encryption_algorithm = Column(String(50), default="AES-256-GCM")
    encryption_salt = Column(LargeBinary, nullable=False)
    encryption_iv = Column(LargeBinary, nullable=False)
    
    # Metadata
    is_active = Column(Boolean, default=True)
    last_rotated_at = Column(String)
    created_by = Column(String(256))
    
    def __repr__(self):
        return f"<EncryptedCredential {self.provider_type}/{self.credential_name}>"
