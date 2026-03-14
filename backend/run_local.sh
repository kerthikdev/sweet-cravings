#!/bin/bash
# run_local.sh — Start all microservices locally (no Docker required)

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# ── Check .env ─────────────────────────────────────────────────────────────
if [ ! -f .env ]; then
  echo "❌  .env not found. Run 'make init' first and set your MONGO_URI."
  exit 1
fi

# Load env vars
export $(grep -v '^#' .env | xargs)

if [[ "$MONGO_URI" == *"YOUR_USER"* ]]; then
  echo "❌  MONGO_URI in backend/.env still has placeholder values."
  echo "    Update it with your real MongoDB Atlas connection string."
  exit 1
fi

# ── Service URLs (localhost for local mode) ────────────────────────────────
export USER_SERVICE_URL=http://localhost:5001
export PRODUCT_SERVICE_URL=http://localhost:5002
export ORDER_SERVICE_URL=http://localhost:5003
export PAYMENT_SERVICE_URL=http://localhost:5004

# ── Virtual environment ────────────────────────────────────────────────────
if [ ! -d venv ]; then
  echo "📦 Creating virtual environment..."
  python3 -m venv venv
fi

source venv/bin/activate

echo "📦 Installing dependencies..."
pip install -q Flask pymongo flask-bcrypt PyJWT flask-cors requests

# ── PID tracking file ──────────────────────────────────────────────────────
rm -f .local_pids

start_service() {
  local name=$1
  local dir=$2
  local port=$3
  echo "🚀  Starting $name on port $port..."
  (cd "$dir" && python app.py) &
  echo $! >> .local_pids
}

# ── Start all services ─────────────────────────────────────────────────────
start_service "User Service"    user_service    5001
start_service "Product Service" product_service 5002
start_service "Order Service"   order_service   5003
start_service "Payment Service" payment_service 5004

sleep 1   # Give backend services a moment to start

start_service "API Gateway"     api_gateway     8080

echo ""
echo "✅  All services started!"
echo ""
echo "   API Gateway  →  http://localhost:5050"
echo "   User Service →  http://localhost:5001"
echo "   Products     →  http://localhost:5002"
echo "   Orders       →  http://localhost:5003"
echo "   Payments     →  http://localhost:5004"
echo ""
echo "   Frontend     →  http://localhost:3000  (run 'make frontend' separately)"
echo ""
echo "Press Ctrl+C to stop all services."
echo ""

# ── Graceful shutdown on Ctrl+C ────────────────────────────────────────────
cleanup() {
  echo ""
  echo "Stopping all services..."
  if [ -f .local_pids ]; then
    kill $(cat .local_pids) 2>/dev/null || true
    rm -f .local_pids
  fi
  echo "✅  All services stopped."
  exit 0
}

trap cleanup INT TERM
wait
