from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

ORDER_SERVICE_URL = os.environ.get("ORDER_SERVICE_URL", "http://localhost:5003")

# -------------------- Confirm Payment --------------------
@app.route("/api/payment/confirm/<order_id>", methods=["POST"])
def confirm_payment(order_id):
    username = request.json.get("username") if request.json else None

    # Verify the order exists and belongs to user
    params = {}
    if username:
        params["username"] = username

    order_resp = requests.get(f"{ORDER_SERVICE_URL}/api/orders/{order_id}", params=params)
    if order_resp.status_code != 200:
        return jsonify({"error": "Order not found"}), 404

    # Update order status to Paid
    update_resp = requests.put(
        f"{ORDER_SERVICE_URL}/api/orders/{order_id}",
        json={"status": "Paid"}
    )

    if update_resp.status_code != 200:
        return jsonify({"error": "Failed to update order"}), 500

    updated_order = update_resp.json().get("order", {})
    return jsonify({
        "message": "Payment confirmed",
        "order_id": updated_order.get("order_id"),
        "total": updated_order.get("total"),
        "timestamp": updated_order.get("timestamp")
    }), 200

# -------------------- Fail Payment --------------------
@app.route("/api/payment/fail/<order_id>", methods=["POST"])
def fail_payment(order_id):
    username = request.json.get("username") if request.json else None

    params = {}
    if username:
        params["username"] = username

    order_resp = requests.get(f"{ORDER_SERVICE_URL}/api/orders/{order_id}", params=params)
    if order_resp.status_code != 200:
        return jsonify({"error": "Order not found"}), 404

    update_resp = requests.put(
        f"{ORDER_SERVICE_URL}/api/orders/{order_id}",
        json={"status": "Failed"}
    )

    if update_resp.status_code != 200:
        return jsonify({"error": "Failed to update order"}), 500

    return jsonify({"message": "Payment failed", "order_id": order_id}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=True)
