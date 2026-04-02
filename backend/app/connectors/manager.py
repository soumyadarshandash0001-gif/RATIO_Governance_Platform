"""Model connector manager."""
from typing import Dict, Any, Optional, Tuple
from .universal_connector import ConnectorFactory, ModelConnector


class ModelConnectorManager:
    """Manages model connections and credentials."""
    
    def __init__(self, credential_manager=None):
        self.credential_manager = credential_manager
        self.connectors: Dict[str, ModelConnector] = {}
        self.connector_cache: Dict[str, ModelConnector] = {}
    
    async def register_model(
        self,
        provider_type: str,
        model_identifier: str,
        config: Dict[str, Any],
        model_uuid: str,
    ) -> Tuple[bool, str]:
        """Register and verify model connectivity."""
        try:
            connector = ConnectorFactory.create(
                provider_type,
                model_uuid,
                config
            )
            
            # Verify connectivity
            is_verified, message = await connector.verify_connectivity()
            
            if is_verified:
                self.connectors[model_uuid] = connector
                self.connector_cache[model_uuid] = connector
            
            return is_verified, message
        except Exception as e:
            return False, f"Registration failed: {str(e)}"
    
    def get_connector(self, model_uuid: str) -> Optional[ModelConnector]:
        """Retrieve cached connector."""
        return self.connectors.get(model_uuid)
    
    async def generate(self, model_uuid: str, prompt: str):
        """Generate model response."""
        connector = self.get_connector(model_uuid)
        if not connector:
            raise ValueError(f"Model {model_uuid} not registered")
        
        return await connector.generate(prompt)
