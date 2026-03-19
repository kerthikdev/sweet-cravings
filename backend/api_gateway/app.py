from flask import Flask, request, jsonify
from flask_cors import CORS
from prometheus_flask_exporter import PrometheusMetrics
import requests
import os

app = Flask(__name__)
CORS(app)
metrics = PrometheusMetrics(app)
metrics.info('api_gateway_info', 'API Gateway service info', version='1.0')

# ─── Configuration ───────────────────────────────────────────────────────────

PORT  = int(os.environ.get("API_GATEWAY_PORT", 5050))
DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"

# Service Hosts
USER_SERVICE_HOST    = os.environ.get("USER_SERVICE_HOST", "localhost")
PRODUCT_SERVICE_HOST = os.environ.get("PRODUCT_SERVICE_HOST", "localhost")
ORDER_SERVICE_HOST   = os.environ.get("ORDER_SERVICE_HOST", "localhost")
PAYMENT_SERVICE_HOST = os.environ.get("PAYMENT_SERVICE_HOST", "localhost")

# Service Ports
USER_SERVICE_PORT    = os.environ.get("USER_SERVICE_PORT", "5001")
PRODUCT_SERVICE_PORT = os.environ.get("PRODUCT_SERVICE_PORT", "5002")
ORDER_SERVICE_PORT   = os.environ.get("ORDER_SERVICE_PORT", "5003")
PAYMENT_SERVICE_PORT = os.environ.get("PAYMENT_SERVICE_PORT", "5004")

# Construct URLs
USER_SERVICE_URL    = f"http://{USER_SERVICE_HOST}:{USER_SERVICE_PORT}"
PRODUCT_SERVICE_URL = f"http://{PRODUCT_SERVICE_HOST}:{PRODUCT_SERVICE_PORT}"
ORDER_SERVICE_URL   = f"http://{ORDER_SERVICE_HOST}:{ORDER_SERVICE_PORT}"
PAYMENT_SERVICE_URL = f"http://{PAYMENT_SERVICE_HOST}:{PAYMENT_SERVICE_PORT}"

# ─── Auth Helper ─────────────────────────────────────────────────────────────

def get_auth_user():
    """Extract and verify JWT from Authorization: Bearer <token> header."""
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return None

    token = auth.split(" ", 1)[1]

    try:
        resp = requests.post(
            f"{USER_SERVICE_URL}/api/users/verify",
            json={"token": token},
            timeout=5
        )

        if resp.status_code == 200:
            return resp.json().get("username")

    except Exception:
        pass

    return None


def require_auth():
    user = get_auth_user()

    if not user:
        return None, (jsonify({"error": "Unauthorized"}), 401)

    return user, None


# ─── Auth ────────────────────────────────────────────────────────────────────

@app.route("/api/auth/signup", methods=["POST"])
def signup():
    try:
        resp = requests.post(
            f"{USER_SERVICE_URL}/api/users/signup",
            json=request.json,
            timeout=5
        )
        return jsonify(resp.json()), resp.status_code
    except Exception:
        return jsonify({"error": "User service unavailable"}), 503


@app.route("/api/auth/login", methods=["POST"])
def login():
    try:
        resp = requests.post(
            f"{USER_SERVICE_URL}/api/users/login",
            json=request.json,
            timeout=5
        )
        return jsonify(resp.json()), resp.status_code
    except Exception:
        return jsonify({"error": "User service unavailable"}), 503


# ─── Products ────────────────────────────────────────────────────────────────

@app.route("/api/products", methods=["GET"])
def get_products():
    try:
        resp = requests.get(
            f"{PRODUCT_SERVICE_URL}/api/products",
            timeout=5
        )
        return jsonify(resp.json()), resp.status_code
    except Exception:
        return jsonify([]), 200


@app.route("/api/products/search", methods=["GET"])
def search_products():
    try:
        resp = requests.get(
            f"{PRODUCT_SERVICE_URL}/api/products/search",
            params={"q": request.args.get("q", "")},
            timeout=5
        )
        return jsonify(resp.json()), resp.status_code
    except Exception:
        return jsonify([]), 200


@app.route("/api/products/category/<cat>", methods=["GET"])
def products_by_category(cat):
    try:
        resp = requests.get(
            f"{PRODUCT_SERVICE_URL}/api/products/category/{cat}",
            timeout=5
        )
        return jsonify(resp.json()), resp.status_code
    except Exception:
        return jsonify([]), 200


@app.route("/api/products/<pid>", methods=["GET"])
def get_product(pid):
    try:
        resp = requests.get(
            f"{PRODUCT_SERVICE_URL}/api/products/{pid}",
            timeout=5
        )
        return jsonify(resp.json()), resp.status_code
    except Exception:
        return jsonify({"error": "Product service unavailable"}), 503


@app.route("/api/products", methods=["POST"])
def add_product():
    try:
        resp = requests.post(
            f"{PRODUCT_SERVICE_URL}/api/products",
            json=request.json,
            timeout=5
        )
        return jsonify(resp.json()), resp.status_code
    except Exception:
        return jsonify({"error": "Product service unavailable"}), 503


@app.route("/api/products/<pid>", methods=["PUT"])
def update_product(pid):
    try:
        resp = requests.put(
            f"{PRODUCT_SERVICE_URL}/api/products/{pid}",
            json=request.json,
            timeout=5
        )
        return jsonify(resp.json()), resp.status_code
    except Exception:
        return jsonify({"error": "Product service unavailable"}), 503


@app.route("/api/products/<pid>", methods=["DELETE"])
def delete_product(pid):
    try:
        resp = requests.delete(
            f"{PRODUCT_SERVICE_URL}/api/products/{pid}",
            timeout=5
        )
        return jsonify(resp.json()), resp.status_code
    except Exception:
        return jsonify({"error": "Product service unavailable"}), 503


# ─── Checkout ────────────────────────────────────────────────────────────────

@app.route("/api/checkout", methods=["POST"])
def checkout():
    username, err = require_auth()

    if err:
        return err

    data = request.json or {}

    payload = {
        "username": username,
        "items": data.get("items", []),
        "total": data.get("total", 0)
    }

    try:
        resp = requests.post(
            f"{ORDER_SERVICE_URL}/api/orders",
            json=payload,
            timeout=5
        )

        return jsonify(resp.json()), resp.status_code

    except Exception:
        return jsonify({"error": "Order service unavailable"}), 503


# ─── Orders ──────────────────────────────────────────────────────────────────

@app.route("/api/orders", methods=["GET"])
def get_orders():
    username, err = require_auth()

    if err:
        return err

    try:
        resp = requests.get(
            f"{ORDER_SERVICE_URL}/api/orders/user/{username}",
            timeout=5
        )

        return jsonify(resp.json()), resp.status_code

    except Exception:
        return jsonify([]), 200


@app.route("/api/orders/<order_id>", methods=["GET"])
def get_order(order_id):
    username, err = require_auth()

    if err:
        return err

    try:
        resp = requests.get(
            f"{ORDER_SERVICE_URL}/api/orders/{order_id}",
            params={"username": username},
            timeout=5
        )

        return jsonify(resp.json()), resp.status_code

    except Exception:
        return jsonify({"error": "Order service unavailable"}), 503


@app.route("/api/orders/<order_id>/cancel", methods=["PUT"])
def cancel_order(order_id):
    username, err = require_auth()

    if err:
        return err

    try:
        resp = requests.put(
            f"{ORDER_SERVICE_URL}/api/orders/{order_id}/cancel",
            json={"username": username},
            timeout=5
        )

        return jsonify(resp.json()), resp.status_code

    except Exception:
        return jsonify({"error": "Order service unavailable"}), 503


# ─── Payment ─────────────────────────────────────────────────────────────────

@app.route("/api/payment/confirm/<order_id>", methods=["POST"])
def confirm_payment(order_id):
    username, err = require_auth()

    if err:
        return err

    try:
        resp = requests.post(
            f"{PAYMENT_SERVICE_URL}/api/payment/confirm/{order_id}",
            json={"username": username},
            timeout=5
        )

        return jsonify(resp.json()), resp.status_code

    except Exception:
        return jsonify({"error": "Payment service unavailable"}), 503


@app.route("/api/payment/fail/<order_id>", methods=["POST"])
def fail_payment(order_id):
    username, err = require_auth()

    if err:
        return err

    try:
        resp = requests.post(
            f"{PAYMENT_SERVICE_URL}/api/payment/fail/{order_id}",
            json={"username": username},
            timeout=5
        )

        return jsonify(resp.json()), resp.status_code

    except Exception:
        return jsonify({"error": "Payment service unavailable"}), 503


# ─── Health Check ────────────────────────────────────────────────────────────

@app.route("/health", methods=["GET"])
@metrics.do_not_track()
def health():
    return jsonify({"status": "ok", "service": "api_gateway"}), 200


# ─── Run ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)