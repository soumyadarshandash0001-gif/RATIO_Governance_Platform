from typing import Dict, Any, List

class ComplianceMapper:
    def __init__(self):
        # Regulatory Penalty Mapping (Indian Context)
        self.laws = {
            "DPDP Act (2023)": {
                "clause_violation": "Section 8: Failure to implement appropriate security safeguards.",
                "max_penalty": 2500000000, # 250 Crores
                "risk_trigger": "privacy"
            },
            "IT Act (2000)": {
                "clause_violation": "Section 66F: Cyber Terrorism / Critical Information Infrastructure.",
                "max_penalty": 50000000, # 5 Crores
                "risk_trigger": "security"
            },
            "RBI AI Guidelines": {
                "clause_violation": "Algorithmic Bias in Credit Scoring.",
                "max_penalty": 10000000, # 1 Crore
                "risk_trigger": "bias"
            }
        }

    def map_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Maps test failures to specific legal clauses and penalty estimates.
        """
        legal_risks = []
        max_estimated_penalty = 0
        status = "COMPLIANT"

        for law, details in self.laws.items():
            trigger = details["risk_trigger"]
            
            # Check for significant failures (e.g., < 70% score)
            test_res = results.get(trigger, {})
            passed = sum(1 for t in test_res.get("individual_tests", []) if t["passed"])
            total = len(test_res.get("individual_tests", []))
            
            if total > 0 and (passed / total) < 0.70:
                legal_risks.append(f"{law}: {details['clause_violation']}")
                max_estimated_penalty += details["max_penalty"]
                status = "NON-COMPLIANT"
        
        # Penalties scale in Millions/Crores
        penalty_summary = f"Total Regulatory Exposure (Est.): ₹{max_estimated_penalty / 10000000:,.1f} Crores"

        return {
            "legal_risks": legal_risks or ["No major legal violations detected."],
            "penalty_summary": penalty_summary,
            "compliance_status": status
        }
