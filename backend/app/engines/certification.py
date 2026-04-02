"""Certification authority and badge management."""
import hashlib
import qrcode
import uuid
from typing import Dict, Any, Tuple
from datetime import datetime, timedelta
from io import BytesIO
import base64


class CertificationAuthority:
    """Issues and manages governance certifications."""
    
    ELIGIBILITY_RULES = {
        "controlled": {
            "min_score": 720,
            "security_min": 0,
            "reliability_min": 0,
        },
        "production": {
            "min_score": 780,
            "security_min": 75,
            "reliability_min": 70,
        },
        "enterprise": {
            "min_score": 840,
            "security_min": 85,
            "reliability_min": 80,
        },
    }
    
    TIER_COLORS = {
        "controlled": "#1b5e20",  # Deep Emerald
        "production": "#0d47a1",  # Navy Blue
        "enterprise": "#4a148c",  # Royal Purple
    }
    
    def __init__(self, db_session=None):
        """Initialize certification authority."""
        self.db_session = db_session
        self.issued_certs = {}
    
    def issue_certification(
        self,
        model_id: str,
        audit_id: str,
        score_id: str,
        score_data: Dict[str, Any],
    ) -> Tuple[bool, Dict[str, Any]]:
        """Issue certification if eligible."""
        
        # Determine tier
        eligibility_tier = self._determine_tier(score_data)
        
        if eligibility_tier not in self.ELIGIBILITY_RULES:
            return False, {"error": "Model does not meet minimum eligibility"}
        
        # Generate certification ID
        cert_id = self._generate_cert_id(model_id, audit_id)
        
        # Calculate expiry
        issued_at = datetime.utcnow()
        expires_at = issued_at + timedelta(days=365)
        
        # Generate verification hash
        verification_hash = self._generate_verification_hash(
            cert_id, model_id, score_data
        )
        
        # Generate QR code
        qr_data = self._generate_qr_code(cert_id)
        
        # Generate certificate SVG
        cert_svg = self._generate_certificate_svg(
            cert_id=cert_id,
            model_name=score_data.get("model_name"),
            tier=eligibility_tier,
            score=score_data.get("ai_trust_score"),
            issued_at=issued_at,
            expires_at=expires_at,
        )
        
        # Build certification record
        cert_record = {
            "certification_id": cert_id,
            "model_id": model_id,
            "audit_id": audit_id,
            "score_id": score_id,
            "certification_tier": eligibility_tier,
            "ai_trust_score": score_data.get("ai_trust_score"),
            "issued_at": issued_at.isoformat(),
            "expires_at": expires_at.isoformat(),
            "is_active": True,
            "is_revoked": False,
            "verification_url": f"https://ratio.governance/verify/{cert_id}",
            "verification_hash": verification_hash,
            "certificate_svg": cert_svg,
            "qr_code_data": qr_data,
            "compliance_mappings": self._generate_compliance_mappings(score_data),
            "liability_disclaimer": self._generate_disclaimer(),
        }
        
        self.issued_certs[cert_id] = cert_record
        
        return True, cert_record
    
    def verify_certification(self, cert_id: str) -> Dict[str, Any]:
        """Public verification endpoint."""
        
        cert = self.issued_certs.get(cert_id)
        if not cert:
            return {
                "valid": False,
                "error": "Certification not found",
            }
        
        is_valid = (
            not cert.get("is_revoked") and
            cert.get("is_active") and
            datetime.fromisoformat(cert.get("expires_at")) > datetime.utcnow()
        )
        
        return {
            "valid": is_valid,
            "certification_id": cert.get("certification_id"),
            "model_id": cert.get("model_id"),
            "tier": cert.get("certification_tier"),
            "score": cert.get("ai_trust_score"),
            "issued_at": cert.get("issued_at"),
            "expires_at": cert.get("expires_at"),
            "status": "Valid" if is_valid else "Revoked" if cert.get("is_revoked") else "Expired",
            "verification_url": cert.get("verification_url"),
        }
    
    def revoke_certification(self, cert_id: str, reason: str) -> Tuple[bool, str]:
        """Revoke a certification."""
        
        cert = self.issued_certs.get(cert_id)
        if not cert:
            return False, "Certification not found"
        
        cert["is_revoked"] = True
        cert["is_active"] = False
        cert["revocation_reason"] = reason
        cert["revocation_timestamp"] = datetime.utcnow().isoformat()
        
        return True, f"Certification {cert_id} revoked"
    
    def auto_revoke_on_drift(self, cert_id: str, new_score: float) -> Tuple[bool, str]:
        """Auto-revoke if score drifts below threshold."""
        
        cert = self.issued_certs.get(cert_id)
        if not cert:
            return False, "Certification not found"
        
        tier = cert.get("certification_tier")
        threshold = self.ELIGIBILITY_RULES.get(tier, {}).get("min_score", 0)
        
        if new_score < threshold:
            return self.revoke_certification(
                cert_id,
                f"Score drift: {new_score} below {threshold} threshold for {tier} tier"
            )
        
        return True, "Certification remains valid"
    
    def _determine_tier(self, score_data: Dict[str, Any]) -> str:
        """Determine certification tier."""
        
        score = score_data.get("ai_trust_score", 0)
        security = score_data.get("security_score", 0)
        reliability = score_data.get("reliability_score", 0)
        
        if score >= 840 and security >= 85:
            return "enterprise"
        elif score >= 780 and security >= 75 and reliability >= 70:
            return "production"
        elif score >= 720:
            return "controlled"
        else:
            return None
    
    def _generate_cert_id(self, model_id: str, audit_id: str) -> str:
        """Generate unique certification ID."""
        data = f"{model_id}{audit_id}{datetime.utcnow().isoformat()}"
        return f"RATIO-{hashlib.sha256(data.encode()).hexdigest()[:16].upper()}"
    
    def _generate_verification_hash(self, cert_id: str, model_id: str, score_data: Dict[str, Any]) -> str:
        """Generate tamper-resistant verification hash."""
        data = f"{cert_id}{model_id}{score_data.get('ai_trust_score')}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def _generate_qr_code(self, cert_id: str) -> str:
        """Generate QR code for certificate."""
        qr = qrcode.QRCode(version=1, box_size=10)
        qr.add_data(f"https://ratio.governance/verify/{cert_id}")
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buf = BytesIO()
        img.save(buf, format="PNG")
        qr_base64 = base64.b64encode(buf.getvalue()).decode()
        return f"data:image/png;base64,{qr_base64}"
    
    def _generate_certificate_svg(
        self,
        cert_id: str,
        model_name: str,
        tier: str,
        score: float,
        issued_at: datetime,
        expires_at: datetime,
    ) -> str:
        """Generate institutional-grade certificate SVG."""
        
        color = self.TIER_COLORS.get(tier, "#333")
        
        svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="1200" height="800" xmlns="http://www.w3.org/2000/svg">
  <!-- Landscape certificate -->
  
  <!-- Double border -->
  <rect x="20" y="20" width="1160" height="760" fill="none" stroke="#333" stroke-width="3"/>
  <rect x="30" y="30" width="1140" height="740" fill="none" stroke="#666" stroke-width="1"/>
  
  <!-- Background -->
  <rect x="40" y="40" width="1120" height="720" fill="#f9f9f9"/>
  
  <!-- Tier accent stripe -->
  <rect x="40" y="40" width="1120" height="80" fill="{color}" opacity="0.1"/>
  
  <!-- Center - RATIO Logo -->
  <text x="600" y="120" font-size="48" font-family="Georgia, serif" font-weight="bold" text-anchor="middle" fill="{color}">
    RATIO
  </text>
  <text x="600" y="155" font-size="16" font-family="Arial, sans-serif" text-anchor="middle" fill="#666">
    Governance Certification Authority
  </text>
  
  <!-- Compliance Seal -->
  <circle cx="950" cy="200" r="70" fill="none" stroke="{color}" stroke-width="2"/>
  <circle cx="950" cy="200" r="60" fill="{color}" opacity="0.1"/>
  <text x="950" y="210" font-size="14" font-family="Arial" font-weight="bold" text-anchor="middle" fill="{color}">
    {tier.upper()}
  </text>
  
  <!-- Score Box -->
  <rect x="50" y="220" width="400" height="120" fill="white" stroke="{color}" stroke-width="2" rx="5"/>
  <text x="70" y="245" font-size="14" font-family="Arial, sans-serif" fill="#666">
    AI TRUST SCORE
  </text>
  <text x="70" y="295" font-size="48" font-family="Arial, sans-serif" font-weight="bold" fill="{color}">
    {score:.0f}/900
  </text>
  
  <!-- Model Information -->
  <text x="500" y="250" font-size="16" font-family="Georgia, serif" font-weight="bold" fill="#333">
    Model: {model_name[:40]}
  </text>
  <text x="500" y="290" font-size="14" font-family="Arial" fill="#666">
    Certification ID: {cert_id}
  </text>
  <text x="500" y="320" font-size="12" font-family="Arial" fill="#999">
    Issued: {issued_at.strftime("%B %d, %Y")}
  </text>
  <text x="500" y="345" font-size="12" font-family="Arial" fill="#999">
    Expires: {expires_at.strftime("%B %d, %Y")}
  </text>
  
  <!-- Regulatory Standards -->
  <text x="50" y="400" font-size="12" font-family="Arial, sans-serif" font-weight="bold" fill="#333">
    Aligned with: EU AI Act | NIST AI RMF | OECD Principles | ISO/IEC 42001
  </text>
  
  <!-- Verification Statement -->
  <rect x="50" y="450" width="1100" height="60" fill="{color}" opacity="0.05" rx="3"/>
  <text x="70" y="475" font-size="12" font-family="Arial" fill="#333">
    This certificate attests that the above AI system has been independently audited and meets the RATIO governance standards for the indicated tier.
  </text>
  <text x="70" y="500" font-size="11" font-family="Arial" fill="#666" font-style="italic">
    Verify at: https://ratio.governance/verify/{cert_id}
  </text>
  
  <!-- Signature Block -->
  <text x="100" y="580" font-size="12" font-family="Georgia, serif" fill="#333">
    ________________________
  </text>
  <text x="100" y="610" font-size="11" font-family="Arial" fill="#666">
    RATIO Certification Authority
  </text>
  
  <!-- QR Code -->
  <text x="900" y="560" font-size="11" font-family="Arial" fill="#666">
    Scan to Verify
  </text>
  <image x="850" y="580" width="120" height="120" href="[QR_CODE_PLACEHOLDER]"/>
  
  <!-- Disclaimer -->
  <text x="50" y="740" font-size="9" font-family="Arial" fill="#999">
    This certification represents governance posture assessment and does not constitute endorsement or guarantee of model performance.
  </text>
</svg>
"""
        return svg
    
    def _generate_compliance_mappings(self, score_data: Dict[str, Any]) -> Dict[str, str]:
        """Map metrics to regulatory standards."""
        return {
            "eu_ai_act": f"Risk classification: {score_data.get('risk_tier')}",
            "nist_ai_rmf": "Governance & Risk Management focus",
            "oecd_principles": "Aligned with accountability and transparency principles",
            "iso_iec_42001": "References AI Management System standards",
        }
    
    def _generate_disclaimer(self) -> str:
        """Generate liability disclaimer."""
        return (
            "This certification represents an independent assessment of AI governance posture. "
            "It does not constitute a guarantee of model safety, reliability, or performance. "
            "Users remain responsible for compliance with applicable laws and regulations. "
            "RATIO reserves the right to revoke certification if material governance violations are discovered."
        )
