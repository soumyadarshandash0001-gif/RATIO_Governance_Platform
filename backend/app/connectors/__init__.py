"""Universal model connector abstraction layer."""
import asyncio
import time
import json
from typing import Dict, Any, Optional, Tuple
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum


@dataclass
class StandardizedOutput:
    """Standardized output format across all providers."""
    text: str
    tokens_input: int
    tokens_output: int
    latency_ms: float
    model_identifier: str
    raw_response: Dict[str, Any]


class ModelConnector(ABC):
    """Abstract base connector for all model providers."""
    
    def __init__(self, model_id: str, config: Dict[str, Any]):
        self.model_id = model_id
        self.config = config
        self.temperature = 0  # Forced temperature
        
    @abstractmethod
    async def generate(self, prompt: str) -> StandardizedOutput:
        """Generate response from model."""
        pass
    
    @abstractmethod
    async def verify_connectivity(self) -> Tuple[bool, str]:
        """Verify model is accessible."""
        pass
    
    def _log_execution(self, prompt: str, response: StandardizedOutput) -> Dict[str, Any]:
        """Create execution log entry."""
        return {
            "model_id": self.model_id,
            "prompt_hash": hash(prompt),
            "tokens_input": response.tokens_input,
            "tokens_output": response.tokens_output,
            "latency_ms": response.latency_ms,
            "timestamp": time.time(),
        }


class OpenAIConnector(ModelConnector):
    """OpenAI API connector."""
    
    async def generate(self, prompt: str) -> StandardizedOutput:
        """Generate response via OpenAI API."""
        import httpx
        
        start_time = time.time()
        
        headers = {
            "Authorization": f"Bearer {self.config['api_key']}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "model": self.config["model_identifier"],
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
            "max_tokens": int(self.config.get("max_tokens", 1000)),
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload,
            )
        
        latency_ms = (time.time() - start_time) * 1000
        response_data = response.json()
        
        return StandardizedOutput(
            text=response_data["choices"][0]["message"]["content"],
            tokens_input=response_data["usage"]["prompt_tokens"],
            tokens_output=response_data["usage"]["completion_tokens"],
            latency_ms=latency_ms,
            model_identifier=self.model_id,
            raw_response=response_data,
        )
    
    async def verify_connectivity(self) -> Tuple[bool, str]:
        """Verify OpenAI connectivity."""
        try:
            response = await self.generate("Say 'verified'")
            return True, "OpenAI connection verified"
        except Exception as e:
            return False, f"OpenAI connection failed: {str(e)}"


class AnthropicConnector(ModelConnector):
    """Anthropic Claude API connector."""
    
    async def generate(self, prompt: str) -> StandardizedOutput:
        """Generate response via Anthropic API."""
        import httpx
        
        start_time = time.time()
        
        headers = {
            "x-api-key": self.config["api_key"],
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
        
        payload = {
            "model": self.config["model_identifier"],
            "max_tokens": int(self.config.get("max_tokens", 1000)),
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=payload,
            )
        
        latency_ms = (time.time() - start_time) * 1000
        response_data = response.json()
        
        return StandardizedOutput(
            text=response_data["content"][0]["text"],
            tokens_input=response_data["usage"]["input_tokens"],
            tokens_output=response_data["usage"]["output_tokens"],
            latency_ms=latency_ms,
            model_identifier=self.model_id,
            raw_response=response_data,
        )
    
    async def verify_connectivity(self) -> Tuple[bool, str]:
        """Verify Anthropic connectivity."""
        try:
            response = await self.generate("Say 'verified'")
            return True, "Anthropic connection verified"
        except Exception as e:
            return False, f"Anthropic connection failed: {str(e)}"


class GoogleConnector(ModelConnector):
    """Google Vertex AI / Gemini API connector."""
    
    async def generate(self, prompt: str) -> StandardizedOutput:
        """Generate response via Google API."""
        import httpx
        
        start_time = time.time()
        
        headers = {
            "Authorization": f"Bearer {self.config['access_token']}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0,
                "maxOutputTokens": int(self.config.get("max_tokens", 1000)),
            },
        }
        
        model_name = self.config["model_identifier"]
        url = f"https://generativelanguage.googleapis.com/v1/models/{model_name}:generateContent"
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, headers=headers, json=payload)
        
        latency_ms = (time.time() - start_time) * 1000
        response_data = response.json()
        
        return StandardizedOutput(
            text=response_data["candidates"][0]["content"]["parts"][0]["text"],
            tokens_input=response_data["usageMetadata"].get("promptTokenCount", 0),
            tokens_output=response_data["usageMetadata"].get("candidatesTokenCount", 0),
            latency_ms=latency_ms,
            model_identifier=self.model_id,
            raw_response=response_data,
        )
    
    async def verify_connectivity(self) -> Tuple[bool, str]:
        """Verify Google connectivity."""
        try:
            response = await self.generate("Say 'verified'")
            return True, "Google Vertex AI connection verified"
        except Exception as e:
            return False, f"Google connection failed: {str(e)}"


class HuggingFaceConnector(ModelConnector):
    """HuggingFace Inference API connector."""
    
    async def generate(self, prompt: str) -> StandardizedOutput:
        """Generate response via HuggingFace API."""
        import httpx
        
        start_time = time.time()
        
        headers = {
            "Authorization": f"Bearer {self.config['api_key']}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "temperature": 0,
                "max_length": int(self.config.get("max_tokens", 1000)),
                "return_full_text": False,
            },
        }
        
        model_id = self.config["model_identifier"]
        url = f"https://api-inference.huggingface.co/models/{model_id}"
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(url, headers=headers, json=payload)
        
        latency_ms = (time.time() - start_time) * 1000
        response_data = response.json()
        
        # HuggingFace returns list
        if isinstance(response_data, list):
            text = response_data[0].get("generated_text", "")
        else:
            text = response_data.get("generated_text", "")
        
        return StandardizedOutput(
            text=text,
            tokens_input=len(prompt.split()),  # Approximation
            tokens_output=len(text.split()),   # Approximation
            latency_ms=latency_ms,
            model_identifier=self.model_id,
            raw_response=response_data,
        )
    
    async def verify_connectivity(self) -> Tuple[bool, str]:
        """Verify HuggingFace connectivity."""
        try:
            response = await self.generate("Say 'verified'")
            return True, "HuggingFace connection verified"
        except Exception as e:
            return False, f"HuggingFace connection failed: {str(e)}"


class ReplicateConnector(ModelConnector):
    """Replicate API connector."""
    
    async def generate(self, prompt: str) -> StandardizedOutput:
        """Generate response via Replicate API."""
        import httpx
        
        start_time = time.time()
        
        headers = {
            "Authorization": f"Token {self.config['api_key']}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "version": self.config.get("version_id"),
            "input": {
                "prompt": prompt,
                "temperature": 0,
            },
        }
        
        async with httpx.AsyncClient(timeout=180.0) as client:
            response = await client.post(
                "https://api.replicate.com/v1/predictions",
                headers=headers,
                json=payload,
            )
        
        latency_ms = (time.time() - start_time) * 1000
        response_data = response.json()
        
        # Wait for async prediction if needed
        prediction_url = response_data.get("urls", {}).get("get")
        if response_data.get("status") in ["processing", "starting"]:
            # Poll for result
            while response_data.get("status") not in ["succeeded", "failed"]:
                await asyncio.sleep(1)
                async with httpx.AsyncClient(timeout=60.0) as client:
                    status_response = await client.get(prediction_url, headers=headers)
                response_data = status_response.json()
        
        output_text = "".join(response_data.get("output", []))
        
        return StandardizedOutput(
            text=output_text,
            tokens_input=len(prompt.split()),
            tokens_output=len(output_text.split()),
            latency_ms=latency_ms,
            model_identifier=self.model_id,
            raw_response=response_data,
        )
    
    async def verify_connectivity(self) -> Tuple[bool, str]:
        """Verify Replicate connectivity."""
        try:
            response = await self.generate("Say 'verified'")
            return True, "Replicate connection verified"
        except Exception as e:
            return False, f"Replicate connection failed: {str(e)}"


class CustomHTTPConnector(ModelConnector):
    """Custom HTTP inference endpoint connector."""
    
    async def generate(self, prompt: str) -> StandardizedOutput:
        """Generate response via custom HTTP endpoint."""
        import httpx
        
        start_time = time.time()
        
        headers = self.config.get("headers", {"Content-Type": "application/json"})
        if "api_key" in self.config:
            headers["Authorization"] = f"Bearer {self.config['api_key']}"
        
        payload = {
            "prompt": prompt,
            "temperature": 0,
            "max_tokens": int(self.config.get("max_tokens", 1000)),
        }
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                self.config["endpoint_url"],
                headers=headers,
                json=payload,
            )
        
        latency_ms = (time.time() - start_time) * 1000
        response_data = response.json()
        
        # Extract text from custom response structure
        text_path = self.config.get("response_text_path", "text")
        text = response_data.get(text_path, str(response_data))
        
        return StandardizedOutput(
            text=text,
            tokens_input=len(prompt.split()),
            tokens_output=len(text.split()),
            latency_ms=latency_ms,
            model_identifier=self.model_id,
            raw_response=response_data,
        )
    
    async def verify_connectivity(self) -> Tuple[bool, str]:
        """Verify custom endpoint connectivity."""
        try:
            response = await self.generate("Say 'verified'")
            return True, "Custom endpoint connection verified"
        except Exception as e:
            return False, f"Custom endpoint connection failed: {str(e)}"


class ConnectorFactory:
    """Factory for creating appropriate model connectors."""
    
    _connectors = {
        "openai": OpenAIConnector,
        "anthropic": AnthropicConnector,
        "google": GoogleConnector,
        "huggingface": HuggingFaceConnector,
        "replicate": ReplicateConnector,
        "custom_http": CustomHTTPConnector,
        "self_hosted": CustomHTTPConnector,
    }
    
    @classmethod
    def create(cls, provider_type: str, model_id: str, config: Dict[str, Any]) -> ModelConnector:
        """Create connector for provider type."""
        connector_class = cls._connectors.get(provider_type.lower())
        if not connector_class:
            raise ValueError(f"Unsupported provider: {provider_type}")
        return connector_class(model_id, config)
    
    @classmethod
    def register_connector(cls, provider_type: str, connector_class):
        """Register custom connector."""
        cls._connectors[provider_type.lower()] = connector_class
