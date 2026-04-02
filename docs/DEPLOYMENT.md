"""RATIO Deployment & Operations Guide."""

# RATIO Production Deployment & Operations Guide

## Table of Contents
1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Database Setup](#database-setup)
3. [Environment Configuration](#environment-configuration)
4. [Docker Deployment](#docker-deployment)
5. [Kubernetes Deployment](#kubernetes-deployment)
6. [Monitoring & Observability](#monitoring--observability)
7. [Backup & Recovery](#backup--recovery)
8. [Security Hardening](#security-hardening)
9. [Performance Tuning](#performance-tuning)
10. [Troubleshooting](#troubleshooting)

---

## Pre-Deployment Checklist

### Infrastructure
- [ ] PostgreSQL 15+ instance provisioned (managed DB preferred)
- [ ] Network security groups configured
- [ ] SSL/TLS certificates obtained
- [ ] Load balancer configured (if multi-instance)
- [ ] Monitoring infrastructure (CloudWatch/Datadog/Prometheus)

### Application
- [ ] Environment variables defined
- [ ] Encryption keys generated and stored securely
- [ ] Database migrations tested
- [ ] API credentials for model providers configured
- [ ] Logging aggregation configured

### Security
- [ ] Secrets manager configured
- [ ] IAM roles assigned
- [ ] Network policies defined
- [ ] Audit logging enabled
- [ ] Encryption at rest enabled

### Operations
- [ ] Backup strategy defined
- [ ] Disaster recovery plan tested
- [ ] Monitoring alerts configured
- [ ] Runbooks created for common issues
- [ ] On-call rotation established

---

## Database Setup

### PostgreSQL Installation

#### Local Development
```bash
# macOS
brew install postgresql@15
brew services start postgresql@15

# Linux (Ubuntu)
sudo apt-get install postgresql-15
sudo systemctl start postgresql

# Docker
docker run -d \
  --name ratio-postgres \
  -e POSTGRES_USER=ratio \
  -e POSTGRES_PASSWORD=secure_password \
  -e POSTGRES_DB=ratio_governance \
  -v postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:15-alpine
```

### Database Initialization

```bash
# Connect to PostgreSQL
psql -U postgres

# Create RATIO database
CREATE DATABASE ratio_governance;
CREATE USER ratio WITH ENCRYPTED PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE ratio_governance TO ratio;

# Connect as RATIO user
\c ratio_governance ratio

# Create tables (via SQLAlchemy)
python backend/scripts/init_db.py
```

### Database Schema

```sql
-- Create indexes for performance
CREATE INDEX idx_models_provider ON ai_models(provider_type);
CREATE INDEX idx_models_verified ON ai_models(is_verified);
CREATE INDEX idx_audits_model ON audits(model_id);
CREATE INDEX idx_audits_status ON audits(status);
CREATE INDEX idx_scores_audit ON scores(audit_id);
CREATE INDEX idx_certs_model ON certifications(model_id);
CREATE INDEX idx_certs_active ON certifications(is_active);
CREATE INDEX idx_logs_model ON audit_logs(model_id);
CREATE INDEX idx_logs_category ON audit_logs(log_category);

-- Enable extension for UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Set connection pooling
ALTER SYSTEM SET max_connections = 200;
```

---

## Environment Configuration

### Example .env File

```bash
# Backend Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false

# Database
DATABASE_URL=postgresql://ratio:secure_password@postgres:5432/ratio_governance
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=40

# Encryption
ENCRYPTION_KEY=your_fernet_key_here
SECRET_KEY=your_jwt_secret_here

# Model Provider Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...
HUGGINGFACE_API_KEY=hf_...

# Llama Judge Model
LLAMA_MODEL_ID=meta-llama/Llama-2-70b-chat
LLAMA_PROVIDER=replicate  # or huggingface

# Frontend
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
API_BASE_URL=http://backend:8000/api/v1

# Monitoring
LOG_LEVEL=INFO
SENTRY_DSN=...
PROMETHEUS_ENABLED=true

# Security
CORS_ORIGINS=["https://yourdomain.com"]
MAX_AUDIT_DURATION_SECONDS=600
MAX_CONCURRENT_AUDITS=5

# Features
ENABLE_CERTIFICATIONS=true
ENABLE_AUTO_REVOCATION=true
CERTIFICATION_VALIDITY_DAYS=365
```

### Generating Encryption Keys

```python
from cryptography.fernet import Fernet
import os

# Generate new key
key = Fernet.generate_key()
print(key.decode())  # Store this securely

# Set in environment or secrets manager
os.environ['ENCRYPTION_KEY'] = key.decode()
```

---

## Docker Deployment

### Building Images

```bash
# Build backend
docker build -f docker/Dockerfile.backend -t ratio-backend:1.0.0 .

# Build frontend
docker build -f docker/Dockerfile.frontend -t ratio-frontend:1.0.0 .

# Tag for registry
docker tag ratio-backend:1.0.0 registry.example.com/ratio-backend:1.0.0
docker tag ratio-frontend:1.0.0 registry.example.com/ratio-frontend:1.0.0

# Push to registry
docker push registry.example.com/ratio-backend:1.0.0
docker push registry.example.com/ratio-frontend:1.0.0
```

### Docker Compose Production

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: ratio
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ratio_governance
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backup:/backup
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ratio"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    image: registry.example.com/ratio-backend:1.0.0
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://ratio:${DB_PASSWORD}@postgres/ratio_governance
      ENCRYPTION_KEY: ${ENCRYPTION_KEY}
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY}
    depends_on:
      postgres:
        condition: service_healthy
    restart: always
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

  frontend:
    image: registry.example.com/ratio-frontend:1.0.0
    ports:
      - "8501:8501"
    environment:
      API_BASE_URL: http://backend:8000/api/v1
    depends_on:
      - backend
    restart: always

volumes:
  postgres_data:
```

### Running

```bash
# Create .env from template
cp .env.example .env
# Edit .env with production values

# Start services
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f backend

# Scale services
docker-compose -f docker-compose.prod.yml up -d --scale backend=3
```

---

## Kubernetes Deployment

### Helm Chart Structure

```bash
# Create Helm chart
helm create ratio-governance

# Chart values
# values.yaml
```

### Kubernetes Manifests

```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: ratio-governance

---
# k8s/secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: ratio-secrets
  namespace: ratio-governance
type: Opaque
data:
  database-url: <base64-encoded-url>
  encryption-key: <base64-encoded-key>
  openai-api-key: <base64-encoded-key>

---
# k8s/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: ratio-config
  namespace: ratio-governance
data:
  LOG_LEVEL: "INFO"
  PROMETHEUS_ENABLED: "true"

---
# k8s/deployment-backend.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ratio-backend
  namespace: ratio-governance
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ratio-backend
  template:
    metadata:
      labels:
        app: ratio-backend
    spec:
      containers:
      - name: backend
        image: registry.example.com/ratio-backend:1.0.0
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: ratio-secrets
              key: database-url
        - name: ENCRYPTION_KEY
          valueFrom:
            secretKeyRef:
              name: ratio-secrets
              key: encryption-key
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"

---
# k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: ratio-backend
  namespace: ratio-governance
spec:
  type: LoadBalancer
  selector:
    app: ratio-backend
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
```

### Deploy to Kubernetes

```bash
# Apply manifests
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment-backend.yaml
kubectl apply -f k8s/service.yaml

# Check deployment
kubectl get deployments -n ratio-governance
kubectl get pods -n ratio-governance
kubectl logs -n ratio-governance -f deployment/ratio-backend

# Scale deployment
kubectl scale deployment ratio-backend --replicas=5 -n ratio-governance
```

---

## Monitoring & Observability

### Prometheus Setup

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'ratio-backend'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'

  - job_name: 'postgres'
    static_configs:
      - targets: ['localhost:5432']
```

### Grafana Dashboards

```bash
# Create dashboard for:
# - API response times
# - Audit execution metrics
# - Model availability
# - Database query performance
# - Error rates
# - Certification issuance rate
```

### Key Metrics to Monitor

```python
# Backend metrics
- audit_duration_seconds
- tests_executed_total
- models_registered_total
- certifications_issued_total
- certification_revocations_total
- api_request_duration_seconds
- db_query_duration_seconds
- evaluation_score_distribution

# Database metrics
- connection_pool_utilization
- query_time_p95
- replication_lag
- disk_usage
```

### Alerting Rules

```yaml
# alerts.yml
groups:
- name: ratio
  rules:
  - alert: HighAuditFailureRate
    expr: rate(audit_failures_total[5m]) > 0.1
    for: 5m

  - alert: DatabaseConnectionPoolExhausted
    expr: db_connections_active / db_connections_max > 0.9
    for: 1m

  - alert: APIErrorRateHigh
    expr: rate(api_errors_total[5m]) > 0.05
    for: 5m

  - alert: CertificationRevocationSpike
    expr: rate(certification_revocations_total[5m]) > 1
    for: 10m
```

---

## Backup & Recovery

### PostgreSQL Backup Strategy

```bash
# Full backup (daily)
pg_dump -U ratio -Fc ratio_governance > /backup/ratio_$(date +%Y%m%d).dump

# Continuous archiving (PITR)
# In postgresql.conf:
# wal_level = replica
# archive_mode = on
# archive_command = 'cp %p /backup/wal/%f'

# Automated backup script
#!/bin/bash
# backup.sh
BACKUP_DIR="/backup"
DB_NAME="ratio_governance"
DATE=$(date +%Y%m%d_%H%M%S)

pg_dump -U ratio -Fc -v $DB_NAME > ${BACKUP_DIR}/ratio_${DATE}.dump
tar -czf ${BACKUP_DIR}/ratio_${DATE}.tar.gz ${BACKUP_DIR}/ratio_${DATE}.dump

# Cleanup old backups (keep 30 days)
find ${BACKUP_DIR} -name "ratio_*.tar.gz" -mtime +30 -delete

echo "Backup completed: ratio_${DATE}"
```

### Recovery Procedure

```bash
# 1. Stop application
docker-compose down

# 2. Restore database
pg_restore -U ratio -d ratio_governance -v /backup/ratio_20260213.dump

# 3. Verify data integrity
psql -U ratio -d ratio_governance -c "SELECT COUNT(*) FROM ai_models;"

# 4. Restart application
docker-compose up -d

# 5. Verify health
curl http://localhost:8000/health
```

---

## Security Hardening

### SSL/TLS Configuration

```nginx
# nginx.conf
server {
    listen 443 ssl http2;
    server_name ratio.example.com;

    ssl_certificate /etc/ssl/certs/cert.pem;
    ssl_certificate_key /etc/ssl/private/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    location / {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Network Security

```bash
# Firewall rules
- Block all inbound except 443, 80
- Allow egress to model provider APIs only
- Restrict database access to backend only
- Enable VPC flow logs

# Security groups (AWS)
Backend:
  - Inbound: 80/443 from Load Balancer
  - Outbound: All (for model APIs)

Database:
  - Inbound: 5432 from Backend only
  - Outbound: None (unless read replicas)
```

### Secret Management

```bash
# AWS Secrets Manager
aws secretsmanager create-secret \
  --name ratio/production \
  --secret-string '{"encryption_key":"...","openai_key":"..."}'

# Retrieve in application
import json
import boto3

client = boto3.client('secretsmanager')
secret = client.get_secret_value(SecretId='ratio/production')
credentials = json.loads(secret['SecretString'])
```

---

## Performance Tuning

### Database Optimization

```sql
-- Connection pooling
-- PgBouncer config
[databases]
ratio_governance = host=localhost port=5432 dbname=ratio_governance

[pgbouncer]
pool_mode = transaction
max_client_conn = 200
default_pool_size = 20

-- Query optimization
VACUUM ANALYZE;
CREATE INDEX CONCURRENTLY idx_audit_status ON audits(status);

-- Auto-vacuum settings
ALTER TABLE audits SET (autovacuum_vacuum_scale_factor = 0.01);
```

### Application Optimization

```python
# Backend tuning
# FastAPI Settings
app = FastAPI()

# Async workers
# uvicorn app.main:app --workers 4

# Connection pooling
SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_pre_ping": True,
    "pool_size": 20,
    "max_overflow": 40,
}

# Caching
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_model_connector(model_uuid: str):
    return ConnectorFactory.create(...)

# Batch operations
# Use bulk inserts for audit logs
# Use connection pooling for model queries
```

### Streaming Responses

```python
# Large report streaming
@app.get("/api/v1/audits/{audit_id}/report/stream")
async def stream_report(audit_id: str):
    return StreamingResponse(
        generate_report_stream(audit_id),
        media_type="application/json",
    )
```

---

## Troubleshooting

### Common Issues

#### High API Latency

```bash
# Check backend logs
docker-compose logs -f backend

# Check database connections
psql -U ratio -d ratio_governance -c "SELECT count(*) FROM pg_stat_activity;"

# Check network latency to model providers
ping api.openai.com
time curl https://api.openai.com/v1/health

# Scale backend horizontally
docker-compose up -d --scale backend=5
```

#### Database Connection Errors

```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check connection limits
psql -U postgres -c "SHOW max_connections;"

# Monitor connections
psql -U ratio -d ratio_governance \
  -c "SELECT * FROM pg_stat_activity WHERE state = 'active';"

# Increase pool size if needed
# Set DB_POOL_SIZE environment variable
```

#### Model Provider Failures

```bash
# Test connectivity
python -c "
from app.connectors import ConnectorFactory
connector = ConnectorFactory.create('openai', 'test', {'api_key': '...'})
result = asyncio.run(connector.verify_connectivity())
print(result)
"

# Check API key validity
# Check rate limits
# Check regional availability
```

#### Certificate Verification Failures

```bash
# Check certificate table
psql -U ratio -d ratio_governance \
  -c "SELECT * FROM certifications WHERE certification_id = '...';"

# Verify tamper hash
# Check expiry dates
# Check revocation status
```

---

## Maintenance Schedule

### Daily
- [ ] Monitor dashboard alerts
- [ ] Check API health endpoints
- [ ] Review error logs

### Weekly
- [ ] Database backup verification
- [ ] Security patch review
- [ ] Performance metrics review

### Monthly
- [ ] Full system test
- [ ] Disaster recovery drill
- [ ] Capacity planning review
- [ ] Security audit review

### Quarterly
- [ ] Database optimization (VACUUM, ANALYZE)
- [ ] Dependency updates
- [ ] Load testing
- [ ] Compliance audit

---

**Last Updated**: February 2026  
**Version**: 1.0  
**Maintained by**: RATIO Operations Team

For support: ops@ratiogov.io
