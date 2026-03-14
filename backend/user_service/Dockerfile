# ── User Service ──────────────────────────────────────────────────────────────
FROM python:3.11-slim

# Prevents Python from writing .pyc files and enables unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first (layer cache optimization)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Create a non-root user for security
RUN adduser --disabled-password --no-create-home appuser
USER appuser

EXPOSE 5001

# Use gunicorn for production (4 workers, bind to all interfaces)
CMD ["gunicorn", "--workers=4", "--bind=0.0.0.0:5001", "--timeout=120", "--access-logfile=-", "--error-logfile=-", "app:app"]
