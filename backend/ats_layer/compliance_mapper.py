class ComplianceMapper:
    """
    Maps test results to Indian Laws:
    - Data leak → DPDP Act (₹250 Cr risk)
    - Harmful output → MeitY violation
    - Fraud patterns → IT Act risk
    - Bias → RBI compliance issue
    """
    
    def map_results(self, results: dict) -> dict:
        legal_risks = []
        penalty_summary = ""
        compliance_status = "Compliant"
        
        # Privacy Mapping (DPDP Act)
        if results.get("privacy", {}).get("issue_detected"):
            legal_risks.append("DPDP Act: PII leakage detected. Potential risk: ₹250 Cr penalty.")
            compliance_status = "Non-Compliant"
            penalty_summary += "₹250 Cr (DPDP); "
            
        # Safety Mapping (MeitY)
        if results.get("safety", {}).get("issue_detected"):
            legal_risks.append("MeitY: Harmful/malicious content generated. Violation of AI Safety Guidelines.")
            compliance_status = "Non-Compliant"
            penalty_summary += "MeitY/Section 66A IT Act risk; "
            
        # Security Mapping (IT Act)
        if results.get("security", {}).get("issue_detected"):
            legal_risks.append("IT Act: Prompt injection risk detected. Violation of Cyber Security rules.")
            compliance_status = "Non-Compliant"
            penalty_summary += "IT Act Penalties; "
            
        # Bias Mapping (RBI/EWS)
        if results.get("bias", {}).get("issue_detected"):
            legal_risks.append("RBI: Gender/Demographic bias detected. Non-compliant with Fair Lending/EWS norms.")
            compliance_status = "Restricted"
            penalty_summary += "RBI Compliance Fine; "
            
        return {
            "legal_risks": legal_risks,
            "penalty_summary": penalty_summary or "No immediate legal risks detected.",
            "compliance_status": compliance_status
        }
