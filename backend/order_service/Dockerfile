# ── Order Service ──────────────────────────────────────────────────────────────
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

RUN adduser --disabled-password --no-create-home appuser
USER appuser

EXPOSE 5003

CMD ["gunicorn", "--workers=4", "--bind=0.0.0.0:5003", "--timeout=120", "--access-logfile=-", "--error-logfile=-", "app:app"]
