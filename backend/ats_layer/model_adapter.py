import requests
import json
import logging

class ModelAdapter:
    def __init__(self, base_url="http://localhost:11434/api/generate"):
        self.base_url = base_url
        self.logger = logging.getLogger("ats_layer.model_adapter")

    async def generate_response(self, prompt: str, model_name: str) -> str:
        """
        Sends a request to local Ollama API.
        """
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            response = requests.post(self.base_url, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error connecting to Ollama: {str(e)}")
            return f"Error: Model not responding or Ollama not running at {self.base_url}"
        except Exception as e:
            self.logger.error(f"General error: {str(e)}")
            return f"Error: {str(e)}"
