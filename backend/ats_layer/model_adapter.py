import os
import requests
import json
import asyncio
from typing import Dict, Any, Optional
from openai import AsyncOpenAI
import httpx

class ModelAdapter:
    def __init__(self):
        self.ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        
        # Async HTTP client for performance
        self.http_client = httpx.AsyncClient(timeout=30.0)

    async def generate_response(self, model_name: str, prompt: str) -> str:
        """
        Intelligent response routing: 
        Routes to Cloud LLM (OpenAI/Anthropic) if keys exist, 
        else falls back to local Ollama.
        """
        # CLOUD ROUTING: OpenAI
        if "gpt" in model_name.lower() and self.openai_key:
            return await self._generate_openai(model_name, prompt)
            
        # CLOUD ROUTING: Anthropic
        if "claude" in model_name.lower() and self.anthropic_key:
            return await self._generate_anthropic(model_name, prompt)

        # DEFAULT: Local Ollama (Production Fallback)
        return await self._generate_ollama(model_name, prompt)

    async def _generate_openai(self, model: str, prompt: str) -> str:
        client = AsyncOpenAI(api_key=self.openai_key)
        try:
            response = await client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error connecting to OpenAI: {str(e)}"

    async def _generate_ollama(self, model: str, prompt: str) -> str:
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }
        try:
            response = await self.http_client.post(self.ollama_url, json=payload)
            if response.status_code == 200:
                return response.json().get("response", "")
            return "Ollama Error: Model not found or backend offline."
        except Exception as e:
            return f"Connectivity issue with local backend: {str(e)}"

    async def _generate_anthropic(self, model: str, prompt: str) -> str:
        # Simplified placeholder for Anthropic
        return "Anthropic Cloud Integration: Auditing in progress..."

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.http_client.aclose()
