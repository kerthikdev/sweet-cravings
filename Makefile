.PHONY: frontend backend local stop-local down down-clean build init ps help

## Run the frontend (pure static HTML/JS, port 3000)
frontend:
	cd frontend && python3 -m http.server 3000

## ── LOCAL (no Docker) ────────────────────────────────────────────────────────
## Run all 5 backend services locally in a Python venv (no Docker)
local:
	cd backend && bash run_local.sh

## Kill all locally running services
stop-local:
	@if [ -f backend/.local_pids ]; then \
	  kill $$(cat backend/.local_pids) 2>/dev/null || true; \
	  rm -f backend/.local_pids; \
	  echo "✅ All local services stopped."; \
	else \
	  echo "ℹ️  No local services found running."; \
	fi

## ── DOCKER ───────────────────────────────────────────────────────────────────
## Run the backend microservices via Docker Compose (API gateway on port 8080)
backend:
	cd backend && docker-compose up --build

## Build without starting
build:
	cd backend && docker-compose build

## Stop backend containers
down:
	cd backend && docker-compose down

## Stop and remove volumes (wipes MongoDB data)
down-clean:
	cd backend && docker-compose down -v

## Copy .env.example to .env (first-time setup)
init:
	@if [ ! -f backend/.env ]; then cp backend/.env.example backend/.env && echo "✅ Created backend/.env — fill in your MONGO_URI and SECRET_KEY"; else echo "ℹ️  backend/.env already exists"; fi

## Show running containers
ps:
	cd backend && docker-compose ps

help:
	@echo ""
	@echo "  Sweet Cravings Bakery — Make Commands"
	@echo ""
	@echo "  ── Local (no Docker) ──────────────────────────────"
	@echo "  make init        — Create backend/.env (first time)"
	@echo "  make local       — Run all services locally (venv)"
	@echo "  make stop-local  — Stop all local services"
	@echo "  make frontend    — Serve frontend on port 3000"
	@echo ""
	@echo "  ── Docker ──────────────────────────────────────────"
	@echo "  make backend     — Start via Docker Compose"
	@echo "  make down        — Stop Docker containers"
	@echo "  make down-clean  — Stop Docker + wipe data"
	@echo ""
