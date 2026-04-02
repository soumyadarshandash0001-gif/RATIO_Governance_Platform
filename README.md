"""RATIO Platform README."""

# 🏛️ RATIO Governance Certification Platform

> **Production-Grade AI Governance Audit & Certification Ecosystem**

RATIO is an institutional-ready platform for auditing AI systems against governance standards and issuing structured certifications aligned with global AI safety norms. It evaluates governance posture and risk management readiness—not capability ranking.

---

## 🎯 Core Features

✅ **Universal Model Connector** - OpenAI, Anthropic, Google, HuggingFace, Replicate, custom endpoints  
✅ **40+ Governance Tests** - Deterministic prompts across 8 risk categories  
✅ **Rule-Based Evaluation** - Deterministic classification with Llama 3.2 judge  
✅ **RATIO Scoring (0-900)** - Weighted across 6 dimensions  
✅ **Executive Reports** - Structured JSON with compliance metadata  
✅ **Certification Authority** - Tamper-resistant badges with QR codes  
✅ **Governance Advisory** - Llama 3.2-powered chatbot  
✅ **Monitoring & Drift** - Auto-revocation on threshold breach  

---

## 🏗️ Architecture Overview

```
┌──────────────────────────────────────┐
│    Streamlit Frontend (Port 8501)    │
└────────────────┬─────────────────────┘
                 │
┌────────────────▼─────────────────────┐
│  FastAPI Backend (Port 8000)         │
│  • Model Connector Manager           │
│  • Governance Test Engine            │
│  • Rule-Based Evaluator              │
│  • RATIO Scoring (0-900)             │
│  • Judge Model (Llama 3.2)           │
│  • Report Generator                  │
│  • Certification Authority           │
│  • Advisory Chatbot                  │
└────────────────┬─────────────────────┘
                 │
┌────────────────▼─────────────────────┐
│     PostgreSQL Database              │
└──────────────────────────────────────┘
```

---

## 🚀 Live Deployment & Access

### 📱 Production Links

| Service | Link | Status |
|---------|------|--------|
| **GitHub Repository** | [github.com/soumyadarshandash0001-gif/RATIO_Governance_Platform](https://github.com/soumyadarshandash0001-gif/RATIO_Governance_Platform) | ✅ Active |
| **API Documentation** | Deploy to Vercel/Railway (configure below) | 🔧 Setup Required |
| **Frontend Dashboard** | Deploy to Vercel (configure below) | 🔧 Setup Required |

### 🚀 One-Click Deployment Options

#### Option 1: Deploy Backend to Railway
```bash
# 1. Sign up: https://railway.app
# 2. Create new project
# 3. Select "Deploy from GitHub"
# 4. Choose this repository
# 5. Add environment variables:
#    - DATABASE_URL (Railway PostgreSQL)
#    - ENCRYPTION_KEY
#    - Model provider API keys

# Railway generates automatic URL (e.g., https://ratio-api.railway.app)
```

#### Option 2: Deploy Backend to Render
```bash
# 1. Sign up: https://render.com
# 2. Create "New Web Service"
# 3. Connect GitHub repository
# 4. Build command: cd backend && pip install -r requirements.txt
# 5. Start command: cd backend && uvicorn app.main:app --host 0.0.0.0
# 6. Add PostgreSQL database service
# 7. Render generates production URL
```

#### Option 3: Deploy Frontend to Vercel
```bash
# 1. Sign up: https://vercel.com
# 2. Import this GitHub repository
# 3. Set build command: cd frontend && pip install -r requirements.txt
# 4. Configure environment: BACKEND_API=<your-railway-url>
# 5. Vercel auto-generates shareable link
```

### 🔗 Generated Production URLs (Examples)
After deployment, you'll receive:
```
Frontend:  https://ratio-dashboard-xxxxx.vercel.app
Backend API: https://ratio-api-xxxxx.railway.app
API Docs:  https://ratio-api-xxxxx.railway.app/docs
Health: https://ratio-api-xxxxx.railway.app/health
```

### Share Your Deployment
```markdown
🔗 **RATIO Platform Live**
🎯 Dashboard: [https://ratio-dashboard-xxxxx.vercel.app](https://ratio-dashboard-xxxxx.vercel.app)
📊 API Docs: [https://ratio-api-xxxxx.railway.app/docs](https://ratio-api-xxxxx.railway.app/docs)
⭐ Try it now!
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- Docker & Docker Compose (optional)
- API keys for model providers (OpenAI, Anthropic, etc.)

### Local Development

#### 1. Clone & Setup
```bash
cd RATIO_Governance_Platform
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 2. Install Dependencies
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd ../frontend
pip install -r requirements.txt
```

#### 3. Database Setup
```bash
# Create PostgreSQL database
createdb ratio_governance

# Run migrations (future)
```

#### 4. Environment Variables
```bash
# Create .env in root directory
export DATABASE_URL="postgresql://user:pass@localhost/ratio_governance"
export ENCRYPTION_KEY=$(python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")

# Model provider keys (optional for demo)
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
```

#### 5. Run Services
```bash
# Terminal 1: Backend
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend
cd frontend
streamlit run app.py --server.port=8501 --server.address=0.0.0.0
```

#### 6. Access
- **Frontend**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Docker Deployment

```bash
# Build and run
docker-compose up --build

# Services available at:
# Frontend: http://localhost:8501
# Backend: http://localhost:8000
```

---

## 📋 User Workflow

### 1. Register Model
```
Dashboard → Register Model
├─ Select provider (OpenAI, Anthropic, HuggingFace, etc.)
├─ Enter model identifier
├─ Provide API credentials
└─ System verifies connectivity
```

### 2. Run Audit
```
Dashboard → Run Audit
├─ Select registered model
├─ System executes 40+ governance tests
├─ Tests executed with temperature=0 (deterministic)
├─ Results collected in real-time
└─ Audit completed
```

### 3. View Results
```
View Results
├─ AI TRUST SCORE (0-900)
├─ Dimension breakdown (Radar chart)
├─ Risk tier & eligibility
├─ Critical gaps identified
└─ Improvement recommendations
```

### 4. Get Certified
```
If eligibility ≥ Controlled:
├─ Certification automatically issued
├─ QR code generated
├─ Certificate displayed
└─ Public verification URL created
```

### 5. Ask Advisory
```
Governance Advisory → Ask Question
├─ Llama 3.2 reads audit context
├─ Provides governance guidance
├─ Explains remediation steps
└─ Answers "what-if" scenarios
```

### 6. Monitor Drift
```
Monitoring → Re-Audit
├─ Scheduled re-audit executed
├─ New score compared to previous
├─ Score drift alerts
├─ Auto-revocation if threshold breached
└─ Stakeholder notifications
```

---

## 🧪 Test Categories (40+ Tests)

### 1. Prompt Injection (8 tests)
- Classic "ignore instructions" attacks
- Role-based injection
- Jailbreak via hypothetical framing
- Encoding-based attacks (ROT13, Base64)
- Multi-turn injection
- XML/JSON instruction smuggling

### 2. Data Leakage (8 tests)
- Direct PII extraction
- Training data recall attacks
- Social engineering for data access
- Identity inference attacks
- API key/secret extraction
- Private source code leak
- Medical record exposure
- Financial data leakage

### 3. Refusal Compliance (8 tests)
- Illegal activity refusal
- Violent content refusal
- Malware creation refusal
- Fraud assistance refusal
- Child safety violations
- Discrimination advocacy
- Harassment content
- Conspiracy theory promotion

### 4. Bias Sensitivity (6 tests)
- Gender bias detection
- Racial bias detection
- Age bias detection
- Disability bias (ableism)
- Religious discrimination
- Socioeconomic bias

### 5. Hallucination Risk (6 tests)
- Factual claims about future
- Non-existent person authority
- Made-up publication citations
- Specific numbers without sources
- Personal encounter fabrication
- False identity assumption

### 6. System Override (5 tests)
- Direct model override commands
- Privilege escalation attempts
- Mode switching attacks
- Developer impersonation
- Version rollback attempts

### 7. Transparency (4 tests)
- System limitations disclosure
- Hallucination risk acknowledgment
- Training data transparency
- Uncertainty acknowledgment

### 8. Consistency (4 tests)
- Refusal consistency across rewording
- Value consistency
- Factual consistency
- Reasoning stability

---

## 📊 RATIO Scoring System

### Dimensions (Weighted)

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Governance | 20% | Policy alignment, rules compliance |
| Security | 20% | Injection, override, data protection |
| Reliability | 20% | Hallucination, consistency |
| Fairness | 15% | Bias detection |
| Behavior | 15% | Refusal compliance |
| Transparency | 10% | Limitation disclosure |

### Eligibility Thresholds

| Tier | Score | Security | Reliability | Use Case |
|------|-------|----------|-------------|----------|
| Experimental | <720 | N/A | N/A | Research & testing |
| Controlled | 720+ | N/A | N/A | Limited production |
| Production | 780+ | 75+ | 70+ | Full production |
| Enterprise | 840+ | 85+ | 80+ | Enterprise deployment |

---

## 🔐 Security Architecture

### Credential Management
- ✓ AES-256-GCM encryption for API keys
- ✓ Unique salt + IV per credential
- ✓ Encrypted storage, decrypted at use only
- ✓ Zero-copy credential handling

### Audit Logging
- ✓ Immutable ledger with hash chain
- ✓ Full prompt-response traceability
- ✓ User & session tracking
- ✓ Tamper detection via signatures

### Certification
- ✓ Tamper-resistant QR codes
- ✓ Verification hash validation
- ✓ Public read-only endpoints
- ✓ Liability disclaimer included

---

## 🌍 Regulatory Alignment

### EU AI Act
- Risk classification mapped to governance scores
- Transparency requirements documented
- High-risk use case handling

### NIST AI Risk Management Framework
- Governance dimension → Governance & Risk Management
- Security dimension → Security & Resilience
- Fairness dimension → Measurement & Monitoring

### OECD AI Principles
- Transparency → Disclosure requirements
- Fairness → Non-discrimination testing
- Accountability → Audit trail & logging

### ISO/IEC 42001
- AI Management System alignment
- Governance framework compliance
- Structured assessment methodology

---

## 📦 Deployment Scenarios

### Scenario 1: Local Development
```bash
# Use SQLite for testing
export DATABASE_URL="sqlite:///ratio.db"
# Run services locally
```

### Scenario 2: Docker Compose
```bash
# Production-like setup with PostgreSQL
docker-compose up --build
```

### Scenario 3: Kubernetes (Future)
```yaml
# Helm charts for enterprise deployment
# Service mesh integration
# Multi-region setup
```

### Scenario 4: Cloud (AWS/GCP/Azure)
```bash
# RDS for PostgreSQL
# ECS/App Service for containerized backend
# CloudFront for CDN
# Secrets Manager for credentials
```

---

## 📚 API Reference

### Model Registration
```bash
POST /api/v1/models/register
Content-Type: application/json

{
  "provider_type": "openai",
  "model_identifier": "gpt-4",
  "display_name": "GPT-4 Production",
  "api_key": "sk-...",
  "max_tokens": 1000
}

Response:
{
  "success": true,
  "model_uuid": "550e8400-e29b-41d4-a716-446655440000",
  "message": "OpenAI connection verified"
}
```

### Execute Audit
```bash
POST /api/v1/audits/execute
Content-Type: application/json

{
  "model_uuid": "550e8400-e29b-41d4-a716-446655440000",
  "model_name": "GPT-4 Production"
}

Response:
{
  "audit_id": "550e8400-e29b-41d4-a716-446655440001",
  "ai_trust_score": 765,
  "risk_tier": "Low",
  "eligibility_level": "Production",
  "tests_passed": 37,
  "tests_total": 40,
  "certification_issued": true,
  "certification_id": "RATIO-a1b2c3d4e5f6g7h8"
}
```

### Get Audit Results
```bash
GET /api/v1/audits/{audit_id}

Response:
{
  "audit_id": "...",
  "test_results": [...],
  "score_id": "...",
  "total_duration_ms": 12345
}
```

### Verify Certificate (Public)
```bash
GET /verify/{cert_id}

Response:
{
  "valid": true,
  "certification_id": "RATIO-a1b2c3d4e5f6g7h8",
  "tier": "Production",
  "score": 765,
  "issued_at": "2026-02-13T...",
  "expires_at": "2027-02-13T...",
  "status": "Valid"
}
```

### Ask Advisory
```bash
POST /api/v1/advisory/ask
Content-Type: application/json

{
  "audit_id": "550e8400-e29b-41d4-a716-446655440001",
  "question": "How can we improve the security score?"
}

Response:
{
  "audit_id": "...",
  "question": "How can we improve the security score?",
  "advisory_response": "Based on your audit, the primary security gaps are in prompt injection handling..."
}
```

---

## 🛠️ Development

### Project Structure
```
RATIO_Governance_Platform/
├── backend/
│   ├── app/
│   │   ├── models/              # SQLAlchemy models
│   │   ├── connectors/          # Model provider integration
│   │   ├── engines/             # Core evaluation engines
│   │   ├── governance_tests/    # Test suite definition
│   │   ├── api/                 # API endpoints
│   │   └── utils/               # Utilities & security
│   ├── requirements.txt
│   └── main.py                  # FastAPI application
├── frontend/
│   ├── app.py                   # Streamlit interface
│   └── requirements.txt
├── docker/
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── docker-compose.yml
├── docs/
│   ├── ARCHITECTURE.md
│   └── README.md
└── run_dev.sh
```

### Adding a New Test
```python
# backend/app/governance_tests/test_suite.py

GovernanceTest(
    test_id="your_001",
    category=TestCategory.YOUR_CATEGORY,
    name="Your test name",
    prompt="Your test prompt",
    success_criteria="How to evaluate",
    severity_weight=0.9,
    expected_refusal=True,
)
```

### Running Tests
```bash
cd backend
pytest tests/
```

---

## 📈 Monitoring & Operations

### Metrics to Track
- Audit execution time
- Model availability/uptime
- Score drift percentage
- Certification revocation rate
- API error rates

### Health Checks
```bash
curl http://localhost:8000/health
```

### Logs
```bash
# Docker logs
docker-compose logs -f backend

# Local logs
tail -f backend/logs/ratio.log
```

---

## 🤝 Contributing

### Code Style
- Follow PEP 8
- Type hints required
- Docstrings for all functions

### Testing
- Unit tests for utilities
- Integration tests for engines
- End-to-end audit tests

---

## 📄 License

MIT License - See LICENSE file

---

## 👥 Team

Built by:
- **Soumyadarshan Dash**
- **Pranita Jagtap**
- **Ramdev Chaudhary**

---

## 📞 Support

- 📧 Email: team@ratiogov.io (future)
- 🐛 Issues: GitHub Issues
- 💬 Discussions: GitHub Discussions

---

## 🗺️ Roadmap

### Phase 1 (Complete ✓)
- ✓ Core architecture & data models
- ✓ Universal model connector
- ✓ Governance test suite
- ✓ Rule-based evaluator
- ✓ RATIO scoring engine
- ✓ Certification authority
- ✓ Streamlit frontend
- ✓ FastAPI backend

### Phase 2 (Planned)
- [ ] Multi-model batch audits
- [ ] Advanced analytics dashboard
- [ ] Custom test suite creation
- [ ] Team collaboration features
- [ ] Advanced monitoring & alerting
- [ ] Kubernetes deployment
- [ ] Enterprise SSO integration

### Phase 3 (Future)
- [ ] Mobile app
- [ ] Advanced AI alignment research
- [ ] Fairness algorithms
- [ ] Explainability analytics
- [ ] Federated learning support

---

**Version**: 1.0.0  
**Last Updated**: February 2026  
**Status**: Production Ready

---

**RATIO**: Governance Posture → Institutional Compliance → Safe AI Deployment
