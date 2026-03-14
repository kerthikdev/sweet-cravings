# ── Frontend (static HTML/CSS/JS) ─────────────────────────────────────────────
FROM nginx:1.25-alpine

# Remove default nginx static assets
RUN rm -rf /usr/share/nginx/html/*

# Copy app files
COPY . /usr/share/nginx/html/

# Copy custom nginx config (overrides the default server block only)
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

# Nginx runs in the foreground by default in the official image
CMD ["nginx", "-g", "daemon off;"]
