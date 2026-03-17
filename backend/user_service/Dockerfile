FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Port is set at runtime via USER_SERVICE_PORT env var (default 5001)
ARG USER_SERVICE_PORT=5001
ENV USER_SERVICE_PORT=${USER_SERVICE_PORT}
EXPOSE ${USER_SERVICE_PORT}

# Use shell form so $USER_SERVICE_PORT is expanded at container start
CMD gunicorn --workers=2 --bind=0.0.0.0:${USER_SERVICE_PORT} --timeout=60 app:app