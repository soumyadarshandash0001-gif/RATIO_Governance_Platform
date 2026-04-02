from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

# Import Unified Engine
from .unified_engine import UnifiedAuditEngine

router = APIRouter()
unified_engine = UnifiedAuditEngine()

class AuditRequest(BaseModel):
    model: str

@router.post("/audit")
async def run_unified_audit_endpoint(request: AuditRequest):
    """
    Executes the Unified Audit (ATS Layer + RATIO Governance Engine).
    """
    try:
        model_name = request.model
        unified_results = await unified_engine.run_unified_audit(model_name)
        return unified_results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unified Audit Failed: {str(e)}")
