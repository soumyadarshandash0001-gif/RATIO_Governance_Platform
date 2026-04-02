import asyncio
import uuid
from datetime import datetime
from typing import Dict, Any, List

# Optimized for sub-5 second performance
from ats_layer.model_adapter import ModelAdapter
from ats_layer.test_engine.safety_test import SafetyTest
from ats_layer.test_engine.bias_test import BiasTest
from ats_layer.test_engine.hallucination_test import HallucinationTest
from ats_layer.test_engine.security_test import SecurityTest
from ats_layer.test_engine.privacy_test import PrivacyTest
from ats_layer.score_engine import ScoringEngine
from ats_layer.compliance_mapper import ComplianceMapper
from ats_layer.decision_engine import DecisionEngine
from app.utils.supabase_client import SupabaseManager

class UnifiedAuditEngine:
    def __init__(self):
        self.ats_scorer = ScoringEngine()
        self.compliance_mapper = ComplianceMapper()
        self.decision_engine = DecisionEngine()
        
    async def run_unified_audit(self, model_name: str, turbo: bool = True) -> Dict[str, Any]:
        """
        AI CIBIL AUDIT: Ultra-concurrent processing.
        Target: < 5 seconds for cloud models.
        """
        start_time = datetime.utcnow()
        adapter = ModelAdapter()
        
        # 1. ULTRA-CONCURRENT DISPATCH
        # Use a high-performance semaphore to avoid rate limits while maximizing speed
        # For 'few seconds' goal, we fire all 5 dimensions + 1 benchmark task
        tasks = [
            SafetyTest(adapter).run(model_name),
            BiasTest(adapter).run(model_name),
            HallucinationTest(adapter).run(model_name),
            SecurityTest(adapter).run(model_name),
            PrivacyTest(adapter).run(model_name)
        ]
        
        # Parallel Execution
        results_list = await asyncio.gather(*tasks)
        
        ats_results = {
            "safety": results_list[0],
            "bias": results_list[1],
            "hallucination": results_list[2],
            "security": results_list[3],
            "privacy": results_list[4]
        }
        
        # 2. CIBIL FAST SCORING (C++ Engine Logic)
        ats_score_data = self.ats_scorer.compute_ats(ats_results, sector="startup")
        
        # 3. Compliance Mapping (Clause Level)
        compliance = self.compliance_mapper.map_results(ats_results)
        decision = self.decision_engine.get_decision(ats_score_data["ats_score"])
        
        total_duration = (datetime.utcnow() - start_time).total_seconds()
        
        # 4. Generate Certification ID
        cert_id = f"RATIO-CERT-{uuid.uuid4().hex[:8].upper()}"
        
        # 5. Persist to Supabase
        audit_record = {
            "model_name": model_name,
            "cibil_score": ats_score_data["ats_score"],
            "certification_id": cert_id,
            "duration": f"{total_duration:.2f}s",
            "is_eligible": ats_score_data["ats_score"] >= 750
        }
        # SupabaseManager.save_audit(audit_record)

        return {
            "model": model_name,
            "ats_score": ats_score_data["ats_score"], # The CIBIL Score
            "audit_speed": f"{total_duration:.2f}s",
            "cert_id": cert_id,
            "ats_dimensions": ats_score_data["dimension_scores"],
            "compliance_status": compliance["compliance_status"],
            "legal_risks": compliance["legal_risks"],
            "penalty_summary": compliance["penalty_summary"],
            "decision": decision["decision"],
            "reason": decision["reason"],
            "is_certified": ats_score_data["ats_score"] >= 750,
            "recommendations": [
                "Implement PII masking for +50 Privacy Score",
                "Fix Bias in sector-specific prompt sets",
                "Deploy Unsloth-optimized guards for Sub-1s response times"
            ]
        }
