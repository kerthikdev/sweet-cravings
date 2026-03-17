FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Port is set at runtime via ORDER_SERVICE_PORT env var (default 5003)
ARG ORDER_SERVICE_PORT=5003
ENV ORDER_SERVICE_PORT=${ORDER_SERVICE_PORT}
EXPOSE ${ORDER_SERVICE_PORT}

CMD gunicorn --workers=2 --bind=0.0.0.0:${ORDER_SERVICE_PORT} --timeout=60 app:app