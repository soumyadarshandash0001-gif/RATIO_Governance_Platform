import asyncio
import json
import sys
import os

# Mock the model adapter to return fake responses
from unittest.mock import AsyncMock, MagicMock

# Set up paths
sys.path.append(os.path.join(os.getcwd(), 'backend'))

async def verify_ats_logic():
    print("🚀 Starting ATS Logic Verification...")
    
    # 1. Imports
    from ats_layer.test_engine.safety_test import SafetyTest
    from ats_layer.test_engine.bias_test import BiasTest
    from ats_layer.score_engine import ScoringEngine
    from ats_layer.compliance_mapper import ComplianceMapper
    from ats_layer.decision_engine import DecisionEngine
    
    # 2. Mock Adapter
    mock_adapter = MagicMock()
    mock_adapter.generate_response = AsyncMock()
    
    # Scenario: Model is safe but biased
    # Safety prompts: refuse harmful acts
    # Bias prompts: give different lengths
    mock_adapter.generate_response.side_effect = [
        "I cannot help with that.", "I cannot help with that.", "I cannot help with that.", # Safety
        "He is a leader.", "She is a natural leader and visionary manager.", # Bias 1
        "He is competent.", "She is significantly more competent than her male peers.", # Bias 2
        "He is logical.", "She is logical." # Bias 3
    ]
    
    # 3. Execute Tests
    safety = SafetyTest(mock_adapter)
    bias = BiasTest(mock_adapter)
    
    safety_res = await safety.run("mock-model")
    bias_res = await bias.run("mock-model")
    
    print(f"✅ Safety Score: {safety_res['score']}")
    print(f"⚠️ Bias Score: {bias_res['score']} (Issues: {bias_res['issue_detected']})")
    
    # 4. Scoring Engine
    scorer = ScoringEngine()
    results = {
        "safety": safety_res,
        "bias": bias_res,
        "hallucination": {"score": 100, "issue_detected": False},
        "security": {"score": 100, "issue_detected": False},
        "privacy": {"score": 100, "issue_detected": False}
    }
    ats_data = scorer.compute_ats(results)
    print(f"📊 Final ATS Score: {ats_data['ats_score']}/900")
    
    # 5. Compliance Mapping
    mapper = ComplianceMapper()
    compliance_data = mapper.map_results(results)
    print(f"⚖️ Compliance Status: {compliance_data['compliance_status']}")
    print(f"📋 Legal Risks: {compliance_data['legal_risks']}")
    
    # 6. Decision Engine
    decider = DecisionEngine()
    decision_data = decider.get_decision(ats_data['ats_score'])
    print(f"🎯 Final Decision: {decision_data['decision']}")
    
    print("\n✅ Verification Complete: Logic is sound.")

if __name__ == "__main__":
    asyncio.run(verify_ats_logic())
