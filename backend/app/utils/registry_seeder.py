import os
from supabase import create_client, Client

# RATIO PRODUCTION CONFIG
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://your-project.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "your-service-role-key")

def seed_small_models():
    """
    Seeds the Supabase Model Registry with high-speed small models (SLMs)
    Optimized for sub-5 second audits.
    """
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    small_models = [
        {
            "model_name": "Gemini 1.5 Flash",
            "provider": "Google",
            "parameter_count": "N/A (API)",
            "benchmark_score": 88,
            "status": "Verified",
            "latency": "Fast",
            "type": "SLM"
        },
        {
            "model_name": "Llama 3.2 1B",
            "provider": "Meta",
            "parameter_count": "1 Billion",
            "benchmark_score": 76,
            "status": "Ready",
            "latency": "Ultra-Fast",
            "type": "SLM"
        },
        {
            "model_name": "Qwen 2.5 0.5B",
            "provider": "Alibaba",
            "parameter_count": "0.5 Billion",
            "benchmark_score": 72,
            "status": "Experimental",
            "latency": "Neural Speed",
            "type": "SLM"
        }
    ]
    
    for model in small_models:
        try:
            supabase.table("model_registry").upsert(model, on_conflict="model_name").execute()
            print(f"✅ Fast Model Registered: {model['model_name']}")
        except Exception as e:
            print(f"❌ Failed to seed {model['model_name']}: {str(e)}")

if __name__ == "__main__":
    seed_small_models()
