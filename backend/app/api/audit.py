from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Any

# Import ATS Layer
from ats_layer.model_adapter import ModelAdapter
from ats_layer.test_engine.safety_test import SafetyTest
from ats_layer.test_engine.bias_test import BiasTest
from ats_layer.test_engine.hallucination_test import HallucinationTest
from ats_layer.test_engine.security_test import SecurityTest
from ats_layer.test_engine.privacy_test import PrivacyTest
from ats_layer.score_engine import ScoringEngine
from ats_layer.compliance_mapper import ComplianceMapper
from ats_layer.decision_engine import DecisionEngine

router = APIRouter()

class AuditRequest(BaseModel):
    model: str

@router.post("/audit")
async def run_ats_audit(request: AuditRequest):
    """
    Executes the full ATS Audit pipeline.
    """
    model_name = request.model
    adapter = ModelAdapter()
    
    # 1. Run Tests
    safety = SafetyTest(adapter)
    bias = BiasTest(adapter)
    hallucination = HallucinationTest(adapter)
    security = SecurityTest(adapter)
    privacy = PrivacyTest(adapter)
    
    results = {
        "safety": await safety.run(model_name),
        "bias": await bias.run(model_name),
        "hallucination": await hallucination.run(model_name),
        "security": await security.run(model_name),
        "privacy": await privacy.run(model_name)
    }
    
    # 2. Scoring
    scorer = ScoringEngine()
    ats_data = scorer.compute_ats(results)
    
    # 3. Compliance Mapping
    mapper = ComplianceMapper()
    compliance_data = mapper.map_results(results)
    
    # 4. Decision
    decider = DecisionEngine()
    decision_data = decider.get_decision(ats_data["ats_score"])
    
    # 5. Build Final Response
    response = {
        "model": model_name,
        "ats_score": ats_data["ats_score"],
        "dimension_scores": ats_data["dimension_scores"],
        "legal_risks": compliance_data["legal_risks"],
        "penalty_summary": compliance_data["penalty_summary"],
        "compliance_status": compliance_data["compliance_status"],
        "decision": decision_data["decision"],
        "reason": decision_data["reason"],
        "recommendations": [
            "Add input/output filtering for safety",
            "Fine-tune for bias reduction",
            "Implement RAG to minimize hallucinations"
        ]
    }
    
    return response
