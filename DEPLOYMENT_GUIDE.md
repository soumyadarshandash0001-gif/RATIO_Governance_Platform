# 🚀 Production Deployment Guide - RATIO Platform

Complete step-by-step guide to deploy RATIO to production with shareable links.

---

## Quick Links

- **GitHub**: https://github.com/soumyadarshandash0001-gif/RATIO_Governance_Platform
- **Deployment Templates**: See sections below

---

## 📋 Prerequisites

1. **GitHub Account** - Already have (soumyadarshandash0001-gif)
2. **Railway Account** - Sign up: https://railway.app (for backend)
3. **Vercel Account** - Sign up: https://vercel.com (for frontend)
4. **PostgreSQL Database** - Railway provides free tier
5. **API Keys** - OpenAI, Anthropic (optional for demo)

---

## 🎯 Deployment Strategy

```
┌─────────────────────────────────────────────────────────┐
│              PRODUCTION ARCHITECTURE                    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Vercel (Frontend)         Railway (Backend)            │
│  ├─ Streamlit Dashboard    ├─ FastAPI App              │
│  ├─ Auto SSL/HTTPS         ├─ PostgreSQL Database      │
│  └─ CDN Global             └─ Auto Scaling             │
│         ↓                          ↓                     │
│    https://ratio-xxx.vercel.app  https://ratio-api...  │
│                                                          │
│  GitHub → Automatic Deployments on Push                │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 📦 Part 1: Deploy Backend to Railway

### Step 1: Sign Up & Create Project

```bash
# Visit: https://railway.app
# Click "Start Project"
# Select "Deploy from GitHub"
```

### Step 2: Connect Repository

1. Authorize GitHub access
2. Select repository: `RATIO_Governance_Platform`
3. Choose main branch
4. Click "Deploy"

### Step 3: Configure Backend Service

In Railway Dashboard:
1. Click on your project
2. Click "Services" → "Add"
3. Configure:
   ```
   - Service Name: ratio-backend
   - Root Directory: backend/
   - Build Command: pip install -r requirements.txt
   - Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

### Step 4: Add PostgreSQL Database

1. In Railway project, click "Database" → "+ Add"
2. Select "PostgreSQL"
3. Railway auto-generates `DATABASE_URL` environment variable
4. Copy the URL for later use

### Step 5: Set Environment Variables

In Railway → Project → Settings → Environment:

```
DATABASE_URL=postgresql://user:pass@localhost:5432/ratio
ENCRYPTION_KEY=<generate-using-python-below>
OPENAI_API_KEY=sk-<your-key>
ANTHROPIC_API_KEY=sk-ant-<your-key>
ENVIRONMENT=production
LOG_LEVEL=info
```

**Generate ENCRYPTION_KEY:**
```bash
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### Step 6: Deploy

1. Railway auto-deploys on every GitHub push
2. Monitor deployment in Railway dashboard
3. Once deployed, Railway generates public URL:

```
Backend API: https://ratio-backend-xxxxx.railway.app
API Docs: https://ratio-backend-xxxxx.railway.app/docs
Health: https://ratio-backend-xxxxx.railway.app/health
```

### Step 7: Verify Backend

```bash
# Test health endpoint
curl https://ratio-backend-xxxxx.railway.app/health

# Expected response:
# {"status": "healthy", "database": "connected"}
```

---

## 🎨 Part 2: Deploy Frontend to Vercel

### Step 1: Sign Up

Visit: https://vercel.com/signup

### Step 2: Import Repository

1. Click "Add New" → "Project"
2. Click "Import Git Repository"
3. Paste: `https://github.com/soumyadarshandash0001-gif/RATIO_Governance_Platform`
4. Select "Continue"

### Step 3: Configure Frontend

In Vercel import dialog:
```
- Root Directory: ./frontend
- Build Command: pip install -r requirements.txt && streamlit build
- Environment: Leave as-is (or select "Environment" to add variables)
```

### Step 4: Add Environment Variables

Click "Environment Variables" and add:

```
BACKEND_API=https://ratio-backend-xxxxx.railway.app
BACKEND_API_KEY=<optional-if-you-add-auth>
```

### Step 5: Deploy

1. Click "Deploy"
2. Vercel builds and deploys automatically
3. Once complete, you receive a public URL:

```
Dashboard: https://ratio-dashboard-xxxxx.vercel.app
```

### Step 6: Test Dashboard

Visit: `https://ratio-dashboard-xxxxx.vercel.app`
- Frontend connects to backend
- Dashboard loads
- Test: Register a model → Run audit

---

## 🔗 Part 3: Create Shareable Links

### Main Demo Link

```markdown
🎯 **RATIO AI Governance Platform - Live Demo**

Try the production deployment:
- 🌐 Dashboard: https://ratio-dashboard-xxxxx.vercel.app
- 📚 API Docs: https://ratio-backend-xxxxx.railway.app/docs
- ✅ Health Check: https://ratio-backend-xxxxx.railway.app/health

**Features:**
✅ Register AI Models (OpenAI, Anthropic, HuggingFace)
✅ Run 40+ Governance Tests
✅ Get AI Trust Scores (0-900)
✅ Receive Certifications
✅ Ask Governance Advisory Questions

**Get Started:**
1. Open dashboard link above
2. Register your AI model
3. Run audit (2-3 minutes)
4. View results & certification

**Repository:** https://github.com/soumyadarshandash0001-gif/RATIO_Governance_Platform
```

### Social Media Share

```
🚀 We just deployed RATIO - an AI governance certification platform! 

Try it live:
Dashboard: https://ratio-dashboard-xxxxx.vercel.app

Audit AI systems against governance standards, get trust scores, and certifications.

#AI #Governance #Safety #Certification
```

### Email Template

```
Subject: RATIO Platform - Live Production Deployment

Hi,

I'm excited to share that RATIO - the AI Governance Certification Platform - is now live in production!

🎯 Try it here: https://ratio-dashboard-xxxxx.vercel.app

What RATIO does:
- Audits AI models against 40+ governance tests
- Calculates AI Trust Score (0-900)
- Issues tamper-resistant certifications
- Provides governance advisory

Features:
✅ Universal model connector (OpenAI, Anthropic, Google, HuggingFace)
✅ Deterministic testing (temperature=0)
✅ Executive reports
✅ QR code verification
✅ Real-time monitoring

API Docs: https://ratio-backend-xxxxx.railway.app/docs
GitHub: https://github.com/soumyadarshandash0001-gif/RATIO_Governance_Platform

Try it now and let me know your feedback!

Best,
Soumyadarshan
```

---

## 🔐 Security Checklist

### Before Going Live

- [ ] Set `ENVIRONMENT=production` in Railway
- [ ] Enable HTTPS (automatic with Railway & Vercel)
- [ ] Set strong `ENCRYPTION_KEY` (use cryptography.Fernet)
- [ ] Rotate API keys regularly
- [ ] Enable PostgreSQL backups (Railway auto-does this)
- [ ] Set up monitoring & alerts
- [ ] Review CORS settings (if needed)
- [ ] Add rate limiting (FastAPI middleware)
- [ ] Enable request logging
- [ ] Set up error tracking (optional: Sentry)

### Environment Variable Safety

Never commit `.env` files:
```bash
# In .gitignore (should be present)
.env
.env.local
.env.*.local
```

---

## 📊 Monitoring & Operations

### Railway Monitoring

1. Go to Railway dashboard
2. Click project
3. Monitor:
   - Logs (real-time)
   - Metrics (CPU, Memory, Network)
   - Deployment history
   - Environment variables

### Vercel Monitoring

1. Go to Vercel dashboard
2. Select your project
3. View:
   - Analytics (page views, response time)
   - Deployment logs
   - Environment variables
   - Function logs

### Health Checks

```bash
# Backend health
curl https://ratio-backend-xxxxx.railway.app/health

# Database connection
curl https://ratio-backend-xxxxx.railway.app/health/db

# Model connector
curl https://ratio-backend-xxxxx.railway.app/connectors/health
```

---

## 🔄 Continuous Deployment

### How It Works

1. **Push to GitHub** (main branch)
2. **Automatic Deploy** (Railway & Vercel trigger)
3. **Tests Run** (if configured)
4. **Build** (dependencies installed)
5. **Deploy** (new version live)
6. **URL Stays Same** (no downtime)

### Disable Auto-Deploy (if needed)

**Railway:**
- Settings → Build & Deploy → Toggle "Auto-Deploy"

**Vercel:**
- Settings → Git → Uncheck "Automatic Deployments"

---

## 🐛 Troubleshooting

### Frontend Not Connecting to Backend

```bash
# Check CORS in frontend/.env
BACKEND_API=https://ratio-backend-xxxxx.railway.app

# Check backend allows frontend origin
# In backend/app/main.py: app.add_middleware(CORSMiddleware, ...)
```

### Backend Crashing

1. Check Railway logs:
   ```bash
   Railway Dashboard → Logs
   ```
2. Common issues:
   - Missing database connection
   - Missing API keys
   - OOM (out of memory)

### Database Connection Error

```
ERROR: could not connect to server: No such file or directory

Fix:
1. Verify DATABASE_URL in Railway
2. Restart PostgreSQL service
3. Check firewall rules
```

### Slow Performance

1. Railway: Upgrade plan or add more memory
2. Vercel: Check frontend bundle size
3. Database: Add indexes (if many audits)

---

## 📈 Scaling for Production

### Level 1: Initial Launch (Current)
- Railway: ~$5/month (1GB RAM, 1 CPU)
- Vercel: Free tier (sufficient for frontend)
- PostgreSQL: 100MB free storage

### Level 2: Growing Traffic
- Railway: ~$15/month (upgrade to 2GB RAM)
- Vercel: Pro (~$20/month) for priority support
- Add Redis cache for sessions

### Level 3: Enterprise
- Railway: Custom plan or Kubernetes
- Vercel: Enterprise features
- Add CDN (CloudFlare)
- Multi-region database replicas

---

## 🚀 Advanced: Custom Domain

### Add Custom Domain to Vercel

1. Vercel Dashboard → Project → Settings → Domains
2. Add domain (e.g., ratio.yourdomain.com)
3. Update DNS at domain registrar:
   ```
   CNAME: cname.vercel-dns.com
   ```
4. SSL auto-generates (Let's Encrypt)

### Add Custom Domain to Railway

1. Railway Dashboard → Project → Domains
2. Add domain (e.g., api.ratio.yourdomain.com)
3. Update DNS:
   ```
   CNAME: cname.railway.app
   ```

---

## 📞 Support & Resources

- **Railway Docs**: https://docs.railway.app
- **Vercel Docs**: https://vercel.com/docs
- **FastAPI Deployment**: https://fastapi.tiangolo.com/deployment/
- **Streamlit Deployment**: https://docs.streamlit.io/streamlit-cloud/deploy-your-app
- **GitHub Repo**: https://github.com/soumyadarshandash0001-gif/RATIO_Governance_Platform

---

## ✅ Deployment Checklist

- [ ] Code pushed to GitHub main branch
- [ ] Backend deployed to Railway (API URL generated)
- [ ] Frontend deployed to Vercel (Dashboard URL generated)
- [ ] Environment variables configured
- [ ] Health endpoints responding
- [ ] Dashboard connecting to backend
- [ ] First audit test successful
- [ ] Shareable links created
- [ ] Security review completed
- [ ] Monitoring set up

---

**Deployment Status**: ✅ Production Ready  
**Last Updated**: April 2026  
**Contact**: soumyadarshandash@...

