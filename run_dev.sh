#!/bin/bash

# RATIO Governance Platform - Development Run Script

echo "🏛️  RATIO Governance Certification Platform"
echo "========================================="
echo ""

# Set environment
export PYTHONPATH="${PWD}/backend:${PYTHONPATH}"
export DATABASE_URL="postgresql://ratio:ratio@localhost/ratio_governance"
export ENCRYPTION_KEY=$(python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")

# Backend
echo "▶️  Starting Backend (FastAPI)..."
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

sleep 3

# Frontend
echo "▶️  Starting Frontend (Streamlit)..."
cd ../frontend
streamlit run app.py --server.port=8501 --server.address=0.0.0.0 &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"

echo ""
echo "========================================="
echo "✓ RATIO Platform is running!"
echo "  Backend:  http://localhost:8000"
echo "  Frontend: http://localhost:8501"
echo "  API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"
echo "========================================="

# Wait for processes
wait
