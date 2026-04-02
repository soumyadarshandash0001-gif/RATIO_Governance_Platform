# ATS Audit Layer & Dashboard Integration

This add-on extends the RATIO Governance Platform with automated LLM auditing, AI Trust Scoring (ATS), and Indian Law compliance mapping.

## Features
- **Local LLM Testing**: Connects to Ollama (`http://localhost:11434`) for private audits.
- **5-Dimension Analysis**: Safety, Bias, Hallucination, Security, and Privacy.
- **Legal Risk Mapping**: Maps failures to DPDP Act, IT Act, and RBI guidelines.
- **NVIDIA-Style Dashboard**: Professional dark-mode analytics with radar charts.

## Setup Instructions

### 1. Start Ollama
Ensure Ollama is running locally and the model (e.g., `llama3`) is pulled:
```bash
ollama run llama3
```

### 2. Run Backend
From the root directory:
```bash
cd backend
export PYTHONPATH=$PYTHONPATH:.
uvicorn app.main:app --reload
```

### 3. Open Dashboard
Open the dashboard file in your browser:
`RATIO_Governance_Platform/frontend/dashboard/index.html`

## API Endpoints
- `POST /audit`: Runs the full ATS audit pipeline.
  ```json
  { "model": "llama3" }
  ```

## File Structure
- `/backend/ats_layer/`: Core scoring and test logic.
- `/backend/app/api/audit.py`: FastAPI router.
- `/frontend/dashboard/`: Premium HTML/JS UI.
- `/dataset/test_prompts.json`: Audit datasets.
