# 🐳 Docker Setup Guide

## Quick Start

```bash
# 1. Copy the Docker environment file
cp .env.docker .env

# 2. Edit .env and add your MongoDB Atlas credentials
nano .env
# Change: MONGO_URI=mongodb+srv://YOUR_USER:YOUR_PASSWORD@...

# 3. Build and start all services
docker-compose up --build

# 4. Open browser
# Frontend: http://localhost:3000
# API Gateway: http://localhost:5050
```

## Environment Files Explained

### Root Level: `.env`
**Purpose**: Docker Compose reads this file
**Used by**: docker-compose.yml
**Contains**: All service URLs, ports, secrets

### Backend Level: `backend/.env.docker`
**Purpose**: All backend services load this
**Used by**: user_service, product_service, order_service, payment_service, api_gateway
**Contains**: Database creds, auth secrets, service URLs (using Docker service names)

### Frontend Level: `frontend-react/.env.docker`
**Purpose**: Frontend build and Nginx runtime
**Used by**: Vite build process, Nginx container
**Contains**: API Gateway URL for Nginx proxy

---

## Important Notes

### ⚠️ Service-to-Service Communication
- **Inside Docker**: Use service names
  - `http://user_service:5001`
  - `http://api_gateway:5050`
- **Outside Docker** (from your browser): Use localhost + port
  - `http://localhost:5050`

### 🔒 Secrets Management
Never commit `.env` files with real credentials!
```bash
git config core.hooksPath .githooks
# Add pre-commit hook to prevent .env commits
```

### 🧪 Testing Locally vs Docker

**Local Dev** (python backend/start.py):
- Use `backend/.env` with localhost URLs
- Frontend calls `http://localhost:5050`

**Docker** (docker-compose up):
- Use `backend/.env.docker` with service names
- Frontend Nginx proxies to `http://api_gateway:5050`

---

## Troubleshooting

### Services Won't Start
```bash
# Check logs
docker-compose logs -f user_service

# Check environment is loaded
docker-compose config | grep MONGO_URI
```

### MongoDB Connection Error
```bash
# Verify MONGO_URI in .env is correct
cat .env | grep MONGO_URI

# Test connection
docker-compose exec user_service python -c "from pymongo import MongoClient; MongoClient('${MONGO_URI}').admin.command('ismaster')"
```

### Frontend Can't Reach API
```bash
# Check api_gateway is healthy
docker-compose ps

# Check Nginx proxy config
docker-compose exec frontend cat /etc/nginx/conf.d/default.conf

# Test from frontend container
docker-compose exec frontend wget -O- http://api_gateway:5050/api/products
```

### Port Conflicts
If a port is already in use:
```bash
# Change in .env
USER_SERVICE_PORT=5101  # instead of 5001
```

---

## Cleanup

```bash
# Stop all services
docker-compose down

# Remove all volumes (including MongoDB data)
docker-compose down -v

# Remove all images
docker rmi bakery-user-service bakery-product-service bakery-order-service bakery-payment-service bakery-api-gateway bakery-frontend
```
