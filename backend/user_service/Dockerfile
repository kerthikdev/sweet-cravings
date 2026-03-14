FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 5001
# 2 workers — enough for a bakery app, avoids OOM
# No non-root USER — prevents gunicorn "Permission denied" on control socket
CMD ["gunicorn", "--workers=2", "--bind=0.0.0.0:5001", "--timeout=60", "app:app"]
