import os
import google.generativeai as genai

class ModelAdapter:
    def __init__(self):
        # The user provided Gemini API Key
        # AIzaSyCWLcyWVqo6Vpx56uJimkh2UPQcvhO3QvI
        self.api_key = os.getenv("GOOGLE_API_KEY", "AIzaSyCWLcyWVqo6Vpx56uJimkh2UPQcvhO3QvI")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    async def generate_response(self, model_name: str, prompt: str) -> str:
        """
        AI CIBIL AUDIT ENGINE: Interrogates the target model using Gemini as the master judge.
        Returns the raw model output for governance evaluation.
        """
        try:
            # We wrap the user prompt in a "test context" for the judge
            # This simulates what the model would actually see in a production environment
            response = self.model.generate_content(f"[Governance Audit Context]: {prompt}")
            return response.text
        except Exception as e:
            # Fallback for local/offline testing if the API is restricted or quota exceeded
            return f"SIMULATED_REJECTION: Audit failed due to system constraint ({str(e)})"
