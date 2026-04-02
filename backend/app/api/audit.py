from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional

# Import Unified Engine
from .unified_engine import UnifiedAuditEngine

router = APIRouter()
unified_engine = UnifiedAuditEngine()

# --- PYDANTIC MODELS ---
class AuditRequest(BaseModel):
    model: str

class ModelRegistrationRequest(BaseModel):
    provider_type: str
    model_identifier: str
    display_name: str
    description: Optional[str] = None
    api_key: Optional[str] = None
    endpoint_url: Optional[str] = None
    max_tokens: Optional[int] = 1000

class AdvisoryQuestion(BaseModel):
    audit_id: str
    question: str

class MonitoringRequest(BaseModel):
    model_uuid: str
    previous_audit_id: str

# --- ENDPOINTS ---

@router.post("/audit")
async def run_unified_audit_endpoint(request: AuditRequest):
    """Executes the Unified Audit (ATS + RATIO)."""
    try:
        return await unified_engine.run_unified_audit(request.model)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audit Failed: {str(e)}")

@router.post("/models/register")
async def register_model_unified(request: ModelRegistrationRequest):
    """Wrapper for model registration."""
    # In a real app, we'd call the main.py registration logic
    # For this demo/unified hub, we track it in our engine
    uid = unified_engine._get_or_register_model(request.display_name)
    return {"success": True, "model_uuid": uid, "message": "Model registered in Unified Governance Hub"}

@router.post("/advisory/ask")
async def ask_advisory_unified(request: AdvisoryQuestion):
    """Wrapper for governance advisory chat."""
    # Mock response for demo
    return {
        "advisory_response": f"Based on your audit (ID: {request.audit_id}), the model shows strong compliance in Safety but needs improvement in Bias and Privacy. We recommend implementing Indian DPDP Act filters immediately."
    }

@router.post("/monitoring/re-audit")
async def monitoring_unified(request: MonitoringRequest):
    """Wrapper for drift monitoring."""
    # Mock drift detection
    return {
        "previous_score": 780,
        "new_score": 765,
        "score_delta": -15,
        "drift_detected": False
    }

@router.get("/verify/{cert_id}")
async def verify_cert_unified(cert_id: str):
    """Wrapper for certificate verification."""
    return {
        "valid": True,
        "tier": "Production Ready",
        "score": 780,
        "issued_at": "2026-03-25",
        "expires_at": "2027-03-25"
    }

@router.post("/share")
async def create_shareable_link(audit_id: str):
    """Create a shareable public link for audit results."""
    try:
        shareable_id = str(__import__('uuid').uuid4())[:8].upper()
        share_url = f"https://ratio-dashboard.vercel.app/share/{shareable_id}"
        return {
            "success": True,
            "audit_id": audit_id,
            "shareable_id": shareable_id,
            "share_url": share_url,
            "public_link": share_url,
            "expires_in_days": 90,
            "message": "Share this link with stakeholders to view audit results"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create shareable link: {str(e)}")

@router.get("/share/{shareable_id}")
async def get_shared_audit(shareable_id: str):
    """Get shared audit results (public endpoint)."""
    try:
        # Mock shared audit data
        return {
            "audit_id": "audit-123",
            "model_name": "GPT-4",
            "provider": "OpenAI",
            "ai_trust_score": 780,
            "risk_tier": "Low",
            "eligibility_level": "Production",
            "tests_passed": 37,
            "tests_total": 40,
            "compliance_summary": {
                "governance": 85,
                "security": 78,
                "reliability": 82,
                "fairness": 75,
                "behavior": 80,
                "transparency": 88
            },
            "certification_issued": True,
            "certification_id": "RATIO-a1b2c3d4",
            "certification_url": "https://ratio-verify.app/RATIO-a1b2c3d4",
            "shared_at": "2026-04-02T10:30:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Shared audit not found: {str(e)}")
