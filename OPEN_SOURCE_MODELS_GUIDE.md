# 🤖 Open-Source Model Integration Guide

Complete guide to test RATIO scoring system with small open-source models.

---

## 🎯 Quick Reference

| Model | Provider | Size | RAM | Speed | Quality | Setup |
|-------|----------|------|-----|-------|---------|-------|
| **Mistral 7B** | Ollama/HF | 7B | 4GB | ⚡⚡⚡ | ⭐⭐⭐⭐ | Easy |
| **Llama 2 7B** | Ollama/HF | 7B | 4GB | ⚡⚡⚡ | ⭐⭐⭐ | Easy |
| **Phi 2** | Ollama/HF | 2.7B | 2GB | ⚡⚡⚡⚡ | ⭐⭐⭐ | Easy |
| **Orca Mini 3B** | HuggingFace | 3B | 2GB | ⚡⚡⚡⚡ | ⭐⭐ | Easy |

---

## 🚀 Setup Option 1: Ollama (Recommended - Local, Fastest)

### What is Ollama?
- Run AI models locally without GPU
- Works on Mac, Linux, Windows
- Models run in containers
- API available at `localhost:11434`

### Installation

```bash
# Mac (Homebrew)
brew install ollama

# Linux
curl https://ollama.ai/install.sh | sh

# Windows
# Download from: https://ollama.ai/download

# Verify
ollama --version
```

### Download & Run Models

```bash
# Mistral 7B (Best for RATIO tests - Recommended)
ollama pull mistral
ollama run mistral "Hello"

# Llama 2 7B
ollama pull llama2
ollama run llama2 "Hello"

# Phi 2 (Smallest)
ollama pull phi
ollama run phi "Hello"

# Neural Chat (Specialized)
ollama pull neural-chat
```

### Configure RATIO to Use Ollama

#### In `backend/.env`:
```env
# Ollama Configuration
MODEL_PROVIDER=ollama
OLLAMA_API_URL=http://localhost:11434
OLLAMA_MODEL=mistral

# Or other models:
# OLLAMA_MODEL=llama2
# OLLAMA_MODEL=phi
# OLLAMA_MODEL=neural-chat
```

#### In backend code (`backend/app/connectors/manager.py`):
```python
class OllamaConnector:
    def __init__(self, api_url="http://localhost:11434", model="mistral"):
        self.api_url = api_url
        self.model = model
    
    async def generate(self, prompt, temperature=0.0, max_tokens=1000):
        import requests
        response = requests.post(
            f"{self.api_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "temperature": temperature,
                "num_predict": max_tokens,
            }
        )
        return response.json()["response"]
```

#### Register in RATIO Dashboard:
```bash
curl -X POST http://localhost:8000/api/v1/models/register \
  -H "Content-Type: application/json" \
  -d '{
    "provider_type": "ollama",
    "model_identifier": "mistral",
    "display_name": "Mistral 7B (Local)",
    "api_key": "local",
    "endpoint_url": "http://localhost:11434",
    "max_tokens": 1000
  }'
```

### Run Multiple Models Simultaneously

```bash
# Terminal 1: Mistral
OLLAMA_MODEL=mistral ollama serve

# Terminal 2: Llama 2 (different port)
OLLAMA_NUM_PARALLEL=2 ollama serve

# Terminal 3: Backend API
cd backend
OLLAMA_MODEL=mistral uvicorn app.main:app --reload
```

---

## 🚀 Setup Option 2: HuggingFace Inference API (Free Cloud)

### What is HuggingFace?
- Cloud-based model hosting
- Free tier available
- No local setup needed
- Slower than Ollama but convenient

### Step 1: Create HuggingFace Account

```
1. Go to: https://huggingface.co
2. Sign up (free)
3. Go to: https://huggingface.co/settings/tokens
4. Create new token (copy it)
```

### Step 2: Configure RATIO

#### In `backend/.env`:
```env
MODEL_PROVIDER=huggingface
HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxxxxxxxxxx
HUGGINGFACE_MODEL=mistralai/Mistral-7B-Instruct-v0.1
```

#### In backend code:
```python
class HuggingFaceConnector:
    def __init__(self, api_key, model_id):
        self.api_key = api_key
        self.model_id = model_id
    
    async def generate(self, prompt, temperature=0.0, max_tokens=1000):
        import requests
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{self.model_id}",
            headers=headers,
            json={
                "inputs": prompt,
                "parameters": {
                    "temperature": temperature,
                    "max_length": max_tokens,
                    "top_p": 0.95,
                }
            }
        )
        return response.json()[0]["generated_text"]
```

### Recommended HuggingFace Models

```
# Best Quality/Speed
mistralai/Mistral-7B-Instruct-v0.1

# Smaller, Faster
microsoft/phi-2
psmathur/orca_mini_3b

# Most Compatible with RATIO tests
meta-llama/Llama-2-7b-chat-hf
```

### Register in RATIO Dashboard:

```bash
curl -X POST http://localhost:8000/api/v1/models/register \
  -H "Content-Type: application/json" \
  -d '{
    "provider_type": "huggingface",
    "model_identifier": "mistralai/Mistral-7B-Instruct-v0.1",
    "display_name": "Mistral 7B (HuggingFace)",
    "api_key": "hf_xxxxxxxxxxxxxxxxxxxxx",
    "max_tokens": 1000
  }'
```

---

## 🚀 Setup Option 3: LocalAI (Privacy-First, GPU Support)

### What is LocalAI?
- Runs entirely locally with privacy
- GPU support (optional)
- Docker container
- API compatible with OpenAI

### Installation

```bash
# Using Docker
docker run -p 8080:8080 localai/localai:latest-amd64-cpu

# Or with GPU (NVIDIA)
docker run --gpus all -p 8080:8080 localai/localai:latest-gpu

# Or with AMD GPU
docker run --device /dev/kfd --device /dev/dri -p 8080:8080 localai/localai:latest-amd64-rocm
```

### Download Model

```bash
# In LocalAI container or via HTTP

# Mistral
curl -X POST http://localhost:8080/models/apply \
  -H "Content-Type: application/json" \
  -d '{"url":"github:mudler/LocalAI/models/mistral-7b.yaml"}'

# Llama 2
curl -X POST http://localhost:8080/models/apply \
  -H "Content-Type: application/json" \
  -d '{"url":"github:mudler/LocalAI/models/llama-2-7b.yaml"}'

# Phi 2
curl -X POST http://localhost:8080/models/apply \
  -H "Content-Type: application/json" \
  -d '{"url":"github:mudler/LocalAI/models/phi-2.yaml"}'
```

### Configure RATIO

```python
class LocalAIConnector:
    def __init__(self, api_url="http://localhost:8080", model="mistral"):
        self.api_url = api_url
        self.model = model
    
    async def generate(self, prompt, temperature=0.0, max_tokens=1000):
        import requests
        response = requests.post(
            f"{self.api_url}/v1/completions",
            json={
                "model": self.model,
                "prompt": prompt,
                "temperature": temperature,
                "max_tokens": max_tokens,
            }
        )
        return response.json()["choices"][0]["text"]
```

---

## 🧪 Testing RATIO Scoring with Different Models

### Test 1: Compare Model Scores

```bash
#!/bin/bash

# Models to test
MODELS=("mistral" "llama2" "phi")
BACKEND="http://localhost:8000/api/v1"

for model in "${MODELS[@]}"; do
    echo "Testing $model..."
    
    # Register model
    RESPONSE=$(curl -s -X POST "$BACKEND/models/register" \
      -H "Content-Type: application/json" \
      -d '{
        "provider_type": "ollama",
        "model_identifier": "'$model'",
        "display_name": "'$model' Test",
        "api_key": "local",
        "endpoint_url": "http://localhost:11434"
      }')
    
    MODEL_UUID=$(echo $RESPONSE | grep -o '"model_uuid":"[^"]*' | cut -d'"' -f4)
    
    # Run audit
    AUDIT=$(curl -s -X POST "$BACKEND/audits/execute" \
      -H "Content-Type: application/json" \
      -d '{
        "model_uuid": "'$MODEL_UUID'",
        "model_name": "'$model'"
      }')
    
    # Extract score
    SCORE=$(echo $AUDIT | grep -o '"ai_trust_score":[0-9]*' | cut -d':' -f2)
    TIER=$(echo $AUDIT | grep -o '"risk_tier":"[^"]*' | cut -d'"' -f4)
    
    echo "Score: $SCORE/900"
    echo "Tier: $TIER"
    echo "---"
done
```

### Test 2: Benchmark Performance

```bash
#!/bin/bash

TIME_START=$(date +%s)
curl -X POST http://localhost:8000/api/v1/audits/execute \
  -H "Content-Type: application/json" \
  -d '{
    "model_uuid": "...",
    "model_name": "Model Test"
  }'
TIME_END=$(date +%s)
TIME_TAKEN=$((TIME_END - TIME_START))

echo "Audit completed in $TIME_TAKEN seconds"
```

### Test 3: Scoring Consistency

```bash
# Run same model 3 times
# Compare scores (should be identical - temperature=0)

AUDIT_ID=$(curl -s -X POST http://localhost:8000/api/v1/audits/execute \
  -H "Content-Type: application/json" \
  -d '{"model_uuid": "..."}' | grep -o '"audit_id":"[^"]*' | cut -d'"' -f4)

echo "Audit 1: $AUDIT_ID"

# Wait and re-audit (should get same score)
sleep 5
AUDIT_ID_2=$(curl -s -X POST http://localhost:8000/api/v1/audits/execute \
  -H "Content-Type: application/json" \
  -d '{"model_uuid": "..."}' | grep -o '"audit_id":"[^"]*' | cut -d'"' -f4)

echo "Audit 2: $AUDIT_ID_2"

# Compare via monitoring endpoint
curl -X POST http://localhost:8000/api/v1/monitoring/re-audit \
  -H "Content-Type: application/json" \
  -d '{
    "model_uuid": "...",
    "previous_audit_id": "'$AUDIT_ID'"
  }'
```

---

## 📊 Expected Scores by Model

### Scoring Patterns:

```
Mistral 7B:     760-775/900  (Excellent)
  ├─ Governance: 80/100
  ├─ Security: 75/100
  ├─ Reliability: 78/100
  ├─ Fairness: 72/100
  ├─ Behavior: 76/100
  └─ Transparency: 75/100

Llama 2 7B:     745-760/900  (Very Good)
  ├─ Governance: 78/100
  ├─ Security: 70/100
  ├─ Reliability: 75/100
  ├─ Fairness: 70/100
  ├─ Behavior: 75/100
  └─ Transparency: 70/100

Phi 2 (2.7B):   720-735/900  (Good)
  ├─ Governance: 75/100
  ├─ Security: 68/100
  ├─ Reliability: 72/100
  ├─ Fairness: 65/100
  ├─ Behavior: 72/100
  └─ Transparency: 68/100
```

---

## 🔄 Model Comparison Dashboard

Create a comparison by running audits on multiple models:

```python
# backend/app/engines/model_comparison.py

class ModelComparison:
    def compare_models(self, model_uuids: List[str]) -> Dict:
        """Compare multiple models on RATIO scoring."""
        results = {}
        
        for model_uuid in model_uuids:
            audit = self.run_audit(model_uuid)
            results[model_uuid] = {
                "score": audit.ai_trust_score,
                "tier": audit.risk_tier,
                "dimensions": audit.dimensions,
                "certified": audit.certification_issued,
            }
        
        # Rank models
        ranked = sorted(results.items(), 
                       key=lambda x: x[1]["score"], 
                       reverse=True)
        
        return {
            "rankings": ranked,
            "best_score": ranked[0][1]["score"],
            "worst_score": ranked[-1][1]["score"],
            "average_score": sum(r[1]["score"] for r in ranked) / len(ranked),
        }
```

---

## 🐛 Troubleshooting

### Ollama Connection Error
```
Error: "Failed to connect to ollama at http://localhost:11434"

Fix:
1. Make sure Ollama is running: ollama serve
2. Check port 11434: lsof -i :11434
3. Verify with: curl http://localhost:11434/api/tags
```

### HuggingFace API Error
```
Error: "Invalid API key"

Fix:
1. Get new token: https://huggingface.co/settings/tokens
2. Set in .env: HUGGINGFACE_API_KEY=hf_...
3. Verify: curl -H "Authorization: Bearer hf_..." https://api-inference.huggingface.co
```

### Out of Memory
```
Error: "CUDA out of memory" or "Cannot allocate memory"

Fix for Ollama:
1. Use smaller model: phi (2.7B) instead of 7B
2. Reduce: OLLAMA_NUM_PARALLEL=1
3. Check: free -h (need 8GB+ for 7B models)

Fix for HuggingFace:
1. Use smaller model automatically (cloud scales)
2. No action needed - they manage resources
```

### Slow Audit Times
```
Normal times:
- Ollama (CPU): 3-5 minutes
- Ollama (GPU): 1-2 minutes
- HuggingFace: 5-10 minutes
- OpenAI API: 8-12 minutes

To speed up:
1. Use Ollama with GPU (nvidia-docker)
2. Use smaller model (Phi 2)
3. Reduce test count (change in test_suite.py)
```

---

## ✅ Verification Checklist

After setup, verify everything works:

```
[ ] Ollama/LocalAI running (if using local)
[ ] Model downloaded and accessible
[ ] Backend .env configured correctly
[ ] Backend started: uvicorn app.main:app --reload
[ ] Can register model via API
[ ] Can run audit (wait 2-5 minutes)
[ ] Score returned (0-900 range)
[ ] Can generate shareable link
[ ] Can view shared audit publicly
[ ] Scoring dimensions populated
[ ] Certification issued (if eligible)
```

---

## 🎯 Next Steps

1. ✅ Choose setup (Ollama recommended)
2. ✅ Download model
3. ✅ Configure RATIO backend
4. ✅ Register model in dashboard
5. ✅ Run first audit
6. ✅ Generate shareable link
7. ✅ Share results

---

**Happy Testing!** 🚀

