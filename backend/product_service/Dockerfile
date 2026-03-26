FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py add_products.py ./

# Port is set at runtime via PRODUCT_SERVICE_PORT env var (default 5002)
ARG PRODUCT_SERVICE_PORT=5002
ENV PRODUCT_SERVICE_PORT=${PRODUCT_SERVICE_PORT}
EXPOSE ${PRODUCT_SERVICE_PORT}

CMD gunicorn --workers=1 --bind=0.0.0.0:${PRODUCT_SERVICE_PORT} --timeout=60 app:app