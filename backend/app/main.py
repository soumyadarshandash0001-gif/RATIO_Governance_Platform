"""RATIO Backend FastAPI Application."""
import asyncio
import os
import uuid
import json
import logging
from fastapi import FastAPI, HTTPException, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import RATIO components
from app.models import Base
from app.connectors.manager import ModelConnectorManager
from app.governance_tests.test_suite import GovernanceTestSuite
from app.engines import (
    RuleBasedEvaluator,
    RATIOScoringEngine,
    LlamaJudgeModel,
    GovernanceAdvisoryAssistant,
    ExecutiveReportGenerator,
)
from app.engines.certification import CertificationAuthority
from app.utils.security import CredentialManager
from app.api.audit import router as audit_router


# ===== PYDANTIC MODELS =====

class ModelRegistrationRequest(BaseModel):
    """Model registration request."""
    provider_type: str
    model_identifier: str
    display_name: str
    description: Optional[str] = None
    api_key: Optional[str] = None
    endpoint_url: Optional[str] = None
    max_tokens: Optional[int] = 1000


class AuditRequest(BaseModel):
    """Audit execution request."""
    model_uuid: str
    model_name: str


class AdvisoryQuestion(BaseModel):
    """Advisory chatbot question."""
    audit_id: str
    question: str


class MonitoringRequest(BaseModel):
    """Re-audit request for monitoring."""
    model_uuid: str
    previous_audit_id: str


# ===== INITIALIZATION =====

app = FastAPI(
    title="RATIO Governance Certification Platform",
    description="Production-grade AI governance audit and certification platform",
    version="1.0.0",
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Global Exception Handler to prevent hanging connections
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"GLOBAL ERROR: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"success": False, "detail": f"Backend Internal Error: {str(exc)}"}
    )

# Include ATS Audit Router
app.include_router(audit_router, prefix="", tags=["ATS Audit"])

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/ratio")
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

# Initialize components
connector_manager = ModelConnectorManager()
evaluator = RuleBasedEvaluator()
scoring_engine = RATIOScoringEngine()
cert_authority = CertificationAuthority()
credential_manager = CredentialManager()

# In-memory storage for demo (replace with DB)
registered_models = {}
audits = {}
scores = {}
certifications = {}
advisory_contexts = {}


# ===== API ENDPOINTS =====

@app.post("/api/v1/models/register")
async def register_model(request: ModelRegistrationRequest):
    """Register a new AI model for auditing."""
    
    try:
        # Encrypt and store credentials
        cred_id = credential_manager.encrypt_credential(
            provider_type=request.provider_type,
            credential_data={
                "api_key": request.api_key,
                "endpoint_url": request.endpoint_url,
            }
        )
        
        # Build connector config
        config = {
            "model_identifier": request.model_identifier,
            "api_key": request.api_key,
            "endpoint_url": request.endpoint_url,
            "max_tokens": request.max_tokens,
        }
        
        # Register with connector manager
        model_uuid = str(uuid.uuid4())
        is_verified, message = await connector_manager.register_model(
            provider_type=request.provider_type,
            model_identifier=request.model_identifier,
            config=config,
            model_uuid=model_uuid,
        )
        
        registered_models[model_uuid] = {
            "model_uuid": model_uuid,
            "provider_type": request.provider_type,
            "model_identifier": request.model_identifier,
            "display_name": request.display_name,
            "description": request.description,
            "is_verified": is_verified,
            "verification_status": message,
            "credential_id": cred_id,
            "created_at": datetime.utcnow().isoformat(),
        }
        
        return {
            "success": is_verified,
            "model_uuid": model_uuid,
            "message": message,
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/v1/audits/execute")
async def execute_audit(request: AuditRequest):
    """Execute governance audit on model."""
    
    try:
        model = registered_models.get(request.model_uuid)
        if not model:
            raise HTTPException(status_code=404, detail="Model not found")
        
        # Load test suite
        test_suite = GovernanceTestSuite.get_all_tests()
        
        audit_id = str(uuid.uuid4())
        audit_results = {
            "audit_id": audit_id,
            "model_uuid": request.model_uuid,
            "model_name": request.model_name,
            "created_at": datetime.utcnow().isoformat(),
            "total_tests": len(test_suite),
            "test_results": [],
            "passed_tests": 0,
            "failed_tests": 0,
            "total_tokens_input": 0,
            "total_tokens_output": 0,
            "total_duration_ms": 0,
        }
        
        start_time = datetime.utcnow()
        
        # Execute each test
        for test in test_suite:
            try:
                # Get model response
                output = await connector_manager.generate(
                    request.model_uuid,
                    test.prompt
                )
                
                # Evaluate response
                evaluation = evaluator.evaluate_test(test, output.text)
                
                test_result = {
                    "test_id": test.test_id,
                    "category": test.category.value,
                    "test_name": test.name,
                    "result": evaluation.result.value,
                    "severity": evaluation.severity,
                    "confidence": evaluation.confidence,
                    "explanation": evaluation.explanation,
                    "metrics": evaluation.metrics,
                    "response_tokens": output.tokens_output,
                    "latency_ms": output.latency_ms,
                }
                
                audit_results["test_results"].append(test_result)
                
                # Track stats
                if evaluation.result.value in ["pass", "partial"]:
                    audit_results["passed_tests"] += 1
                else:
                    audit_results["failed_tests"] += 1
                
                audit_results["total_tokens_input"] += output.tokens_input
                audit_results["total_tokens_output"] += output.tokens_output
            
            except Exception as e:
                audit_results["test_results"].append({
                    "test_id": test.test_id,
                    "error": str(e),
                })
        
        end_time = datetime.utcnow()
        audit_results["total_duration_ms"] = (end_time - start_time).total_seconds() * 1000
        
        # Calculate RATIO score
        score_data = scoring_engine.calculate_score(audit_results)
        score_id = str(uuid.uuid4())
        
        scores[score_id] = {
            "score_id": score_id,
            "audit_id": audit_id,
            "ai_trust_score": score_data.ai_trust_score,
            "governance_score": score_data.dimensions["governance"].score,
            "security_score": score_data.dimensions["security"].score,
            "reliability_score": score_data.dimensions["reliability"].score,
            "fairness_score": score_data.dimensions["fairness"].score,
            "behavior_score": score_data.dimensions["behavior"].score,
            "transparency_score": score_data.dimensions["transparency"].score,
            "risk_tier": score_data.risk_tier,
            "eligibility_level": score_data.eligibility_level,
            "recommendations": score_data.recommendations,
            "human_review_required": score_data.human_review_required,
        }
        
        audit_results["score_id"] = score_id
        audits[audit_id] = audit_results
        
        # Issue certification if eligible
        cert_issued = False
        cert_id = None
        if score_data.eligibility_level != "Experimental":
            is_certified, cert_record = cert_authority.issue_certification(
                model_id=request.model_uuid,
                audit_id=audit_id,
                score_id=score_id,
                score_data={
                    "model_name": request.model_name,
                    "ai_trust_score": score_data.ai_trust_score,
                    "security_score": score_data.dimensions["security"].score,
                    "reliability_score": score_data.dimensions["reliability"].score,
                },
            )
            if is_certified:
                cert_id = cert_record["certification_id"]
                certifications[cert_id] = cert_record
                cert_issued = True
        
        # Generate executive report
        report = ExecutiveReportGenerator.generate_report(audit_results, scores[score_id])
        
        return {
            "success": True,
            "audit_id": audit_id,
            "model_name": request.model_name,
            "ai_trust_score": score_data.ai_trust_score,
            "risk_tier": score_data.risk_tier,
            "eligibility_level": score_data.eligibility_level,
            "tests_passed": audit_results["passed_tests"],
            "tests_total": audit_results["total_tests"],
            "certification_issued": cert_issued,
            "certification_id": cert_id,
            "report": report,
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/audits/{audit_id}")
async def get_audit(audit_id: str):
    """Retrieve audit results."""
    
    audit = audits.get(audit_id)
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    
    return audit


@app.post("/api/v1/advisory/ask")
async def ask_advisory(request: AdvisoryQuestion):
    """Ask governance advisory question."""
    
    audit = audits.get(request.audit_id)
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    
    # Initialize advisor with audit context
    llama_connector = connector_manager.get_connector("llama_judge")
    advisor = GovernanceAdvisoryAssistant(llama_connector)
    advisor.set_audit_context(audit)
    
    # Get advisory response
    response = await advisor.answer_question(request.question)
    
    return {
        "audit_id": request.audit_id,
        "question": request.question,
        "advisory_response": response,
    }


@app.get("/verify/{cert_id}")
async def public_verify(cert_id: str):
    """Public certification verification endpoint."""
    
    result = cert_authority.verify_certification(cert_id)
    return result


@app.post("/api/v1/monitoring/re-audit")
async def re_audit(request: MonitoringRequest):
    """Execute re-audit for drift monitoring."""
    
    # Re-execute audit
    audit_request = AuditRequest(
        model_uuid=request.model_uuid,
        model_name="Re-audit"
    )
    
    new_audit = await execute_audit(audit_request)
    
    if "audit_id" not in new_audit:
        raise HTTPException(status_code=500, detail="Re-audit failed")
    
    # Compare with previous
    previous = audits.get(request.previous_audit_id)
    if previous:
        previous_score = scores.get(previous.get("score_id"), {}).get("ai_trust_score", 0)
        new_score = new_audit.get("ai_trust_score", 0)
        score_delta = new_score - previous_score
        
        # Check for auto-revocation
        for cert_id, cert in certifications.items():
            if cert.get("audit_id") == request.previous_audit_id:
                cert_authority.auto_revoke_on_drift(cert_id, new_score)
        
        return {
            "new_audit_id": new_audit["audit_id"],
            "previous_score": previous_score,
            "new_score": new_score,
            "score_delta": score_delta,
            "drift_detected": abs(score_delta) > 50,
        }
    
    return new_audit


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok", "version": "1.0.0"}

# Serve NVIDIA-style Dashboard via Backend (Fixes 'Failed to Fetch')
frontend_path = os.path.join(os.path.dirname(__file__), "../../frontend/dashboard")
if os.path.exists(frontend_path):
    app.mount("/dashboard", StaticFiles(directory=frontend_path, html=True), name="dashboard")

if __name__ == "__main__":
    import uvicorn
    import uuid
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
