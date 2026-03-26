FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Port is set at runtime via API_GATEWAY_PORT env var (default 5050)
ARG API_GATEWAY_PORT=5050
ENV API_GATEWAY_PORT=${API_GATEWAY_PORT}
EXPOSE ${API_GATEWAY_PORT}

CMD gunicorn --workers=1 --bind=0.0.0.0:${API_GATEWAY_PORT} --timeout=60 app:app