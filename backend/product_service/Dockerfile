FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py add_products.py ./
EXPOSE 5002
CMD ["gunicorn", "--workers=2", "--bind=0.0.0.0:5002", "--timeout=60", "app:app"]
