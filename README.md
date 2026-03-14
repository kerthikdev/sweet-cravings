# 🍰 Sweet Cravings Bakery

A fully decoupled bakery e-commerce platform built with microservices.

---

## Project Structure

```
bakingantigravity/
├── frontend/              ← Pure HTML/CSS/JS (no framework)
│   ├── login.html
│   ├── signup.html
│   ├── products.html
│   ├── cart.html
│   ├── payment.html
│   ├── orders.html
│   ├── order_success.html
│   ├── admin.html
│   ├── css/style.css
│   ├── js/
│   │   ├── config.js      ← Set API_BASE URL here
│   │   ├── auth.js
│   │   ├── products.js
│   │   ├── cart.js
│   │   ├── payment.js
│   │   ├── orders.js
│   │   └── admin.js
│   └── images/
│
├── backend/
│   ├── api_gateway/       ← port 8080  (REST JSON + CORS)
│   ├── user_service/      ← port 5001  (Auth + JWT)
│   ├── product_service/   ← port 5002  (Catalogue, auto-seeds on start)
│   ├── order_service/     ← port 5003  (Orders)
│   ├── payment_service/   ← port 5004  (Payment)
│   ├── docker-compose.yml
│   └── .env.example
│
└── Makefile
```

---

## Quick Start

### 1. Set up MongoDB Atlas

Create a free cluster at [MongoDB Atlas](https://www.mongodb.com/atlas). Copy your connection string.

### 2. Configure backend environment

```bash
make init
# Then edit backend/.env:
# MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/bakery
mongodb+srv://Username:Password@db/?appName=mongo
# SECRET_KEY=your-secret-key
```

### 3. Start the backend

```bash
make backend
# API Gateway available at http://localhost:8080
# Products are auto-seeded on first startup
```

### 4. Start the frontend (separate terminal)

```bash
make frontend
# Open http://localhost:3000/login.html
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/signup` | Register |
| POST | `/api/auth/login` | Login → returns JWT |
| GET  | `/api/products` | List all products |
| GET  | `/api/products/search?q=` | Search |
| GET  | `/api/products/category/<cat>` | Filter by category |
| POST | `/api/checkout` | Create order (auth required) |
| GET  | `/api/orders` | User's orders (auth required) |
| PUT  | `/api/orders/<id>/cancel` | Cancel order |
| POST | `/api/payment/confirm/<id>` | Confirm payment |
| POST | `/api/payment/fail/<id>` | Simulate failure |

---

## Auth

JWT is returned on login and stored in `localStorage`. All protected API calls include:
```
Authorization: Bearer <token>
```

## Notes

- **Products are auto-seeded** on `product_service` first start — no need to run any scripts
- **Cart** is stored in browser `localStorage`
- **MongoDB Atlas** is required — no local mongo container
- Change `API_BASE` in `frontend/js/config.js` for production deployments
