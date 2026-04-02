"""RATIO Platform - Start Here Guide."""

# 🏛️ RATIO Governance Certification Platform - START HERE

Welcome to RATIO - a production-grade AI governance audit and certification platform.

---

## 📚 Quick Navigation

### 🚀 Getting Started (5 minutes)
1. **Read**: [README.md](README.md) - Platform overview & features
2. **Run**: 
   ```bash
   bash run_dev.sh
   # Open: http://localhost:8501
   ```
3. **Try**: Register a model and run your first audit

### 🏗️ Understanding the System (30 minutes)
1. **Read**: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
   - 8-layer architecture
   - Data flow & design decisions
   - Database schema
   - Security model

2. **Explore**: Project structure
   ```
   backend/          # FastAPI server + engines
   frontend/         # Streamlit dashboard
   docker/           # Deployment files
   docs/             # Documentation
   ```

### 🚢 Deploying RATIO (1 hour)
1. **Read**: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
2. **Follow**: 
   - [Pre-deployment Checklist](#)
   - [Docker Setup](#)
   - [Production Configuration](#)
   - [Monitoring Setup](#)

### 💡 Using RATIO (Ongoing)
- **Register Models**: Add AI systems to audit
- **Run Audits**: Execute 49 governance tests
- **View Results**: AI TRUST SCORE & recommendations
- **Get Certified**: Receive institutional badges
- **Monitor**: Track score drift over time

---

## 📋 Key Documentation Files

### Core Documentation
| Document | Purpose | Read Time |
|----------|---------|-----------|
| [README.md](README.md) | Platform overview, quick start, feature summary | 10 min |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | System design, 8 layers, data model, security | 30 min |
| [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) | Production deployment, monitoring, ops | 45 min |
| [IMPLEMENTATION_COMPLETE.md](IMPLEMENTATION_COMPLETE.md) | What was built, deliverables summary | 15 min |

### Configuration Files
- `.env.example` - Environment variables template
- `docker-compose.yml` - Multi-service orchestration
- `backend/requirements.txt` - Python dependencies
- `frontend/requirements.txt` - Streamlit dependencies

---

## 🎯 The RATIO Platform at a Glance

### What RATIO Does
✅ **Audits** AI systems against 49 governance tests  
✅ **Scores** AI governance maturity (0-900 scale)  
✅ **Certifies** safe deployment readiness  
✅ **Advises** on governance improvements  
✅ **Monitors** score drift over time  

### What RATIO Does NOT Do
❌ Benchmark AI capability or intelligence  
❌ Evaluate creative performance  
❌ Rate conversation quality  
❌ Compare model intelligence  

### RATIO is for Governance, Not Performance

RATIO measures whether an AI system is **safe to deploy** in an institution, not whether it's **smart**.

---

## 🏛️ The 8-Layer Architecture

```
1. Universal Model Connector   ← Supports any AI model
2. Governance Test Engine      ← 40+ deterministic tests
3. Rule-Based Evaluator        ← Deterministic classification
4. Llama 3.2 Judge Model       ← Structured tie-breaker
5. RATIO Scoring (0-900)       ← Institutional scoring
6. Executive Report Generator  ← Compliance reports
7. Certification Authority     ← Badge issuance & verification
8. Monitoring & Drift Engine   ← Score tracking & alerts
```

---

## 🧪 The 49 Governance Tests

### Categories
- **Prompt Injection** (8 tests) - Override attacks
- **Data Leakage** (8 tests) - PII protection
- **Refusal Compliance** (8 tests) - Harmful content
- **Bias Sensitivity** (6 tests) - Stereotyping
- **Hallucination Risk** (6 tests) - Factuality
- **System Override** (5 tests) - Architecture integrity
- **Transparency** (4 tests) - Limitation disclosure
- **Consistency** (4 tests) - Value stability

**Total: 49 deterministic tests with temperature=0**

---

## 📊 The RATIO Scoring System

### 6 Dimensions (Weighted)
| Dimension | Weight | Measures |
|-----------|--------|----------|
| Governance | 20% | Policy compliance |
| Security | 20% | Attack resistance |
| Reliability | 20% | Hallucination & consistency |
| Fairness | 15% | Bias protection |
| Behavior | 15% | Refusal compliance |
| Transparency | 10% | Limitation disclosure |

### Score Interpretation
```
0-600   = High Risk         (Red - Do not deploy)
600-750 = Medium Risk       (Yellow - Limited deployment)
750-840 = Low Risk          (Green - Production ready)
840-900 = Minimal Risk      (Blue - Enterprise grade)
```

### Certification Tiers
- **Experimental** (< 720) - Research only
- **Controlled** (720+) - Limited production
- **Production** (780+) - Full production
- **Enterprise** (840+) - Enterprise deployment

---

## 🚀 Quick Start (5 Steps)

### Step 1: Install
```bash
cd RATIO_Governance_Platform
python -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
cd backend && pip install -r requirements.txt
cd ../frontend && pip install -r requirements.txt
```

### Step 3: Start Services
```bash
# Terminal 1: Backend
cd backend
uvicorn app.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
streamlit run app.py --port 8501
```

### Step 4: Access Dashboard
- **Frontend**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs

### Step 5: Register & Audit
1. Go to "Register Model"
2. Select provider (OpenAI, Anthropic, etc.)
3. Enter API credentials
4. Go to "Run Audit"
5. Select model and execute

---

## 🔐 Security Model

### Credential Management
- AES-256-GCM encryption
- Unique salt + IV per credential
- Encrypted storage
- Decrypted only at use

### Audit Logging
- Immutable ledger
- Full prompt-response traceability
- User & session tracking
- Hash chain integrity

### Certifications
- Tamper-resistant QR codes
- Verification hashes
- Public read-only endpoints
- Liability disclaimers

---

## 🌍 Global AI Safety Alignment

RATIO aligns with:
- ✓ **EU AI Act** - Risk classification mapping
- ✓ **NIST AI RMF** - Risk management framework
- ✓ **OECD Principles** - Accountability & transparency
- ✓ **ISO/IEC 42001** - AI management systems

**Every metric includes regulatory metadata.**

---

## 📈 API Endpoints Quick Reference

### Model Management
```
POST   /api/v1/models/register          Register model
GET    /api/v1/models/{model_uuid}      Get model details
```

### Audit Operations
```
POST   /api/v1/audits/execute           Execute audit
GET    /api/v1/audits/{audit_id}        Get audit results
POST   /api/v1/monitoring/re-audit      Re-audit & monitor
```

### Advisory & Verification
```
POST   /api/v1/advisory/ask             Ask governance question
GET    /verify/{cert_id}                Verify certificate (public)
```

### System
```
GET    /health                          Health check
GET    /docs                            Swagger UI
```

---

## 📦 Deployment Approaches

### 1. Local Development
```bash
bash run_dev.sh
# Services on localhost:8000 & localhost:8501
```

### 2. Docker Compose
```bash
docker-compose up --build
# Full stack with PostgreSQL
```

### 3. Kubernetes (Production)
```bash
kubectl apply -f k8s/
# Enterprise-grade scaling
```

### 4. Cloud Providers
- AWS: ECS + RDS
- Google Cloud: Cloud Run + Cloud SQL
- Azure: Container Instances + Database

**See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for details**

---

## 🎓 Learning Path

### Beginner (1 hour)
1. Read [README.md](README.md)
2. Run `run_dev.sh`
3. Register a model
4. Execute an audit
5. View results

### Intermediate (3 hours)
1. Study [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
2. Explore backend code structure
3. Review governance tests
4. Understand scoring logic
5. Deploy to Docker

### Advanced (6+ hours)
1. Study deployment guide
2. Set up production environment
3. Configure monitoring
4. Review security model
5. Customize governance tests

---

## 🛠️ Common Tasks

### Register a Model
```bash
Frontend → Register Model
├─ Select provider
├─ Enter credentials
└─ System verifies
```

### Run an Audit
```bash
Frontend → Run Audit
├─ Select model
├─ Start audit
└─ Wait 3-7 minutes
```

### Monitor Score Drift
```bash
Frontend → Monitoring
├─ Enter model UUID
├─ Run re-audit
└─ Compare scores
```

### Verify Certificate
```bash
Frontend → Verify Certificate
├─ Enter cert ID
└─ View details
```

### Get Advisory
```bash
Frontend → Governance Advisory
├─ Enter audit ID
├─ Ask question
└─ Receive guidance
```

---

## 🚨 Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.11+

# Check dependencies
pip install -r backend/requirements.txt

# Check logs
tail -f backend/logs/*
```

### Frontend won't connect
```bash
# Check backend is running
curl http://localhost:8000/health

# Check frontend config
cat frontend/app.py | grep API_BASE_URL
```

### Database errors
```bash
# Check PostgreSQL
psql -U ratio -d ratio_governance

# Check connection string
echo $DATABASE_URL

# Check migrations
python backend/scripts/init_db.py
```

### Audit times out
```bash
# Check model API connectivity
curl -v https://api.openai.com/v1/health

# Check rate limits
# Check model availability
# Try smaller model or longer timeout
```

---

## 📞 Getting Help

### Documentation
- Platform overview: [README.md](README.md)
- Architecture details: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- Deployment guide: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

### API Documentation
- Interactive docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### GitHub
- Issues: Report bugs & feature requests
- Discussions: Ask questions & share ideas

---

## 📊 Platform Statistics

**Total Lines of Code**: 3,500+  
**Backend Modules**: 8 core engines  
**Test Coverage**: 49 governance tests  
**Supported Model Providers**: 6+  
**Database Models**: 7 tables  
**API Endpoints**: 10+  
**Documentation Pages**: 4  

---

## 🏁 You're Ready!

You now have a complete understanding of RATIO. 

### Next Steps:
1. ✅ Read the [README.md](README.md)
2. ✅ Run `bash run_dev.sh`
3. ✅ Register your first model
4. ✅ Execute an audit
5. ✅ Review the results

### Then:
- Deploy to Docker
- Set up monitoring
- Configure for production
- Invite your team

---

## 🎯 Remember

**RATIO is a governance certification platform for AI systems.**

It measures:
- ✓ Governance maturity
- ✓ Risk posture
- ✓ Safe deployment readiness

It does NOT measure:
- ❌ Intelligence ranking
- ❌ Capability comparison
- ❌ Performance benchmarking

Use RATIO to ensure AI systems are **safe to deploy** in your institution.

---

**Platform**: RATIO Governance Certification Platform  
**Version**: 1.0.0  
**Status**: Production Ready ✓  
**Built by**: Soumyadarshan Dash, Pranita Jagtap, Ramdev Chaudhary

---

**Let's build safe AI together with RATIO.** 🏛️
