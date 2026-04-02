# Backend Dockerfile for ATS Audit Layer

FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Add any extra dependencies for ATS Layer
RUN pip install requests pydantic fastapi uvicorn

# Copy application code
COPY backend/app ./app
COPY backend/ats_layer ./ats_layer
COPY dataset ./dataset

# Set environment
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8000

# Run FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
