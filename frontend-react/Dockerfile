# ── Stage 1: Build the React app ─────────────────────────────────────────────
FROM node:22-alpine AS builder

WORKDIR /app

# VITE_API_GATEWAY_URL is intentionally left empty here.
# - Local dev:  Vite proxy handles /api → http://localhost:5050 (set in frontend-react/.env)
# - Docker:     Nginx proxies /api → http://api_gateway:5050   (set via docker-compose env)
# - ECS/Cloud:  Pass the ALB DNS name at build time:
#               docker build --build-arg VITE_API_GATEWAY_URL=https://your-alb.amazonaws.com ...
ARG VITE_API_GATEWAY_URL=""
ENV VITE_API_GATEWAY_URL=${VITE_API_GATEWAY_URL}

COPY package*.json ./
RUN npm ci

COPY . .

RUN npm run build

# ── Stage 2: Serve with Nginx ─────────────────────────────────────────────────
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html

# Use the template so API_GATEWAY_URL env var is substituted at container start
COPY nginx.conf.template /etc/nginx/templates/default.conf.template

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]