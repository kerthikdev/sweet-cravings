from flask import Flask, request, jsonify
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter
import requests
import os

app = Flask(__name__)
metrics = PrometheusMetrics(app)
metrics.info('payment_service_info', 'Payment service info', version='1.0')

payments_confirmed_total = Counter(
    'payment_service_payments_confirmed_total',
    'Total number of successful payment confirmations'
)

payments_failed_total = Counter(
    'payment_service_payments_failed_total',
    'Total number of failed payment attempts'
)

# ─── Configuration ───────────────────────────────────────────────────────────

PORT  = int(os.environ.get("PAYMENT_SERVICE_PORT", 5004))
DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"

# Order service connection
ORDER_SERVICE_HOST = os.environ.get("ORDER_SERVICE_HOST", "localhost")
ORDER_SERVICE_PORT = os.environ.get("ORDER_SERVICE_PORT", "5003")

ORDER_SERVICE_URL = f"http://{ORDER_SERVICE_HOST}:{ORDER_SERVICE_PORT}"


# ───────────────── Confirm Payment ─────────────────
@app.route("/api/payment/confirm/<order_id>", methods=["POST"])
def confirm_payment(order_id):

    data = request.get_json(silent=True) or {}
    username = data.get("username")

    params = {}
    if username:
        params["username"] = username

    try:
        order_resp = requests.get(
            f"{ORDER_SERVICE_URL}/api/orders/{order_id}",
            params=params,
            timeout=5
        )
    except requests.exceptions.RequestException:
        return jsonify({"error": "Order service unavailable"}), 503

    if order_resp.status_code != 200:
        return jsonify({"error": "Order not found"}), 404

    try:
        update_resp = requests.put(
            f"{ORDER_SERVICE_URL}/api/orders/{order_id}",
            json={"status": "Paid"},
            timeout=5
        )
    except requests.exceptions.RequestException:
        return jsonify({"error": "Order update failed"}), 503

    if update_resp.status_code != 200:
        return jsonify({"error": "Failed to update order"}), 500

    updated_order = update_resp.json().get("order", {})

    payments_confirmed_total.inc()

    return jsonify({
        "message": "Payment confirmed",
        "order_id": updated_order.get("order_id"),
        "total": updated_order.get("total"),
        "timestamp": updated_order.get("timestamp")
    }), 200


# ───────────────── Fail Payment ─────────────────
@app.route("/api/payment/fail/<order_id>", methods=["POST"])
def fail_payment(order_id):

    data = request.get_json(silent=True) or {}
    username = data.get("username")

    params = {}
    if username:
        params["username"] = username

    try:
        order_resp = requests.get(
            f"{ORDER_SERVICE_URL}/api/orders/{order_id}",
            params=params,
            timeout=5
        )
    except requests.exceptions.RequestException:
        return jsonify({"error": "Order service unavailable"}), 503

    if order_resp.status_code != 200:
        return jsonify({"error": "Order not found"}), 404

    try:
        update_resp = requests.put(
            f"{ORDER_SERVICE_URL}/api/orders/{order_id}",
            json={"status": "Failed"},
            timeout=5
        )
    except requests.exceptions.RequestException:
        return jsonify({"error": "Order update failed"}), 503

    if update_resp.status_code != 200:
        return jsonify({"error": "Failed to update order"}), 500

    payments_failed_total.inc()

    return jsonify({
        "message": "Payment failed",
        "order_id": order_id
    }), 200


# ───────────────── Health Check ─────────────────
@app.route("/health", methods=["GET"])
@metrics.do_not_track()
def health():
    return jsonify({"status": "ok", "service": "payment_service"}), 200


# ───────────────── Run Server ─────────────────
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)