"""Security utilities for RATIO backend."""
import os
from cryptography.fernet import Fernet
from typing import Dict, Any


class CredentialManager:
    """Manages encrypted credential storage."""
    
    def __init__(self):
        """Initialize credential manager."""
        key = os.getenv("ENCRYPTION_KEY", Fernet.generate_key())
        self.cipher = Fernet(key)
        self.stored_credentials = {}
    
    def encrypt_credential(self, provider_type: str, credential_data: Dict[str, Any]) -> str:
        """Encrypt and store credential."""
        import json
        import uuid
        
        cred_id = str(uuid.uuid4())
        
        # Serialize credential data
        json_data = json.dumps(credential_data).encode()
        
        # Encrypt
        encrypted = self.cipher.encrypt(json_data)
        
        # Store
        self.stored_credentials[cred_id] = {
            "provider_type": provider_type,
            "encrypted_data": encrypted,
        }
        
        return cred_id
    
    def decrypt_credential(self, cred_id: str) -> Dict[str, Any]:
        """Decrypt stored credential."""
        import json
        
        cred = self.stored_credentials.get(cred_id)
        if not cred:
            raise ValueError(f"Credential {cred_id} not found")
        
        encrypted_data = cred["encrypted_data"]
        decrypted = self.cipher.decrypt(encrypted_data)
        
        return json.loads(decrypted.decode())
