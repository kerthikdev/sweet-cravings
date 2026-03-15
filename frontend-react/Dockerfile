# ── Stage 1: Build the React app ─────────────────────────────────────────────
FROM node:22-alpine AS builder

WORKDIR /app

# Build arguments passed from docker-compose.yml
ARG VITE_API_GATEWAY_URL=http://localhost:5050

COPY package*.json ./
RUN npm ci

COPY . .

# Pass the build arg as an environment variable during build
ENV VITE_API_GATEWAY_URL=${VITE_API_GATEWAY_URL}

RUN npm run build

# ── Stage 2: Serve with Nginx ─────────────────────────────────────────────────
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf.template /etc/nginx/templates/default.conf.template

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]