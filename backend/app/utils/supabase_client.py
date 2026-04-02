import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://your-project.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "your-anon-key")

class SupabaseManager:
    _instance = None

    @classmethod
    def get_client(cls) -> Client:
        if cls._instance is None:
            cls._instance = create_client(SUPABASE_URL, SUPABASE_KEY)
        return cls._instance

    @classmethod
    def get_model_registry(cls):
        """
        Pulls registered models from the production Supabase registry.
        """
        client = cls.get_client()
        try:
            response = client.table("model_registry").select("*").execute()
            return response.data
        except Exception as e:
            print(f"Supabase Registry Error: {e}")
            return []

    @classmethod
    def save_audit(cls, audit_data: dict):
        """
        Persists a completed audit record to the cloud.
        """
        client = cls.get_client()
        try:
            client.table("audit_history").insert(audit_data).execute()
            return True
        except Exception as e:
            print(f"Supabase Audit Save Error: {e}")
            return False
