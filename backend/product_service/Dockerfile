# ── Product Service ───────────────────────────────────────────────────────────
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all python files (app.py and add_products.py seed helper)
COPY app.py .
COPY add_products.py .

RUN adduser --disabled-password --no-create-home appuser
USER appuser

EXPOSE 5002

CMD ["gunicorn", "--workers=4", "--bind=0.0.0.0:5002", "--timeout=120", "--access-logfile=-", "--error-logfile=-", "app:app"]
