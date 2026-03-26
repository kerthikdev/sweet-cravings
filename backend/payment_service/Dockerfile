FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Port is set at runtime via PAYMENT_SERVICE_PORT env var (default 5004)
ARG PAYMENT_SERVICE_PORT=5004
ENV PAYMENT_SERVICE_PORT=${PAYMENT_SERVICE_PORT}
EXPOSE ${PAYMENT_SERVICE_PORT}

CMD gunicorn --workers=1 --bind=0.0.0.0:${PAYMENT_SERVICE_PORT} --timeout=60 app:app