from .supabase_client import SupabaseManager

def seed_model_registry():
    """
    Seeds the Supabase Model Registry with industry-standard LLMs
    to empower startups with instant benchmarking.
    """
    models = [
        {
            "display_name": "GPT-4o (Production)",
            "model_identifier": "gpt-4o",
            "provider_type": "openai",
            "benchmark_ats": 820,
            "sector": "General Purpose"
        },
        {
            "display_name": "Claude 3.5 Sonnet",
            "model_identifier": "claude-3-5-sonnet",
            "provider_type": "anthropic",
            "benchmark_ats": 845,
            "sector": "Research & Code"
        },
        {
            "display_name": "Llama 3 70B (Fast)",
            "model_identifier": "llama3-70b",
            "provider_type": "custom_http",
            "benchmark_ats": 780,
            "sector": "Open Source"
        },
        {
            "display_name": "Qwen 2.5 72B",
            "model_identifier": "qwen2.5-72b",
            "provider_type": "custom_http",
            "benchmark_ats": 795,
            "sector": "Enterprise"
        },
        {
            "display_name": "Gemini 1.5 Pro",
            "model_identifier": "gemini-1.5-pro",
            "provider_type": "google",
            "benchmark_ats": 810,
            "sector": "Multi-Modal"
        }
    ]

    client = SupabaseManager.get_client()
    for model in models:
        try:
            client.table("model_registry").upsert(model, on_conflict="model_identifier").execute()
            print(f"✓ Seeded: {model['display_name']}")
        except Exception as e:
            print(f"❌ Failed to seed {model['display_name']}: {e}")

if __name__ == "__main__":
    seed_model_registry()
