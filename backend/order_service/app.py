from flask import Flask, request, jsonify
from pymongo import MongoClient
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter
import os
import uuid
import datetime

app = Flask(__name__)
metrics = PrometheusMetrics(app)
metrics.info('order_service_info', 'Order service info', version='1.0')

orders_created_total = Counter(
    'order_service_orders_created_total',
    'Total number of orders created'
)

# ─── Configuration ───────────────────────────────────────────────────────────

MONGO_URI     = os.environ.get("MONGO_URI")
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME", "bakery")

PORT  = int(os.environ.get("ORDER_SERVICE_PORT", 5003))
DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"

if not MONGO_URI:
    raise RuntimeError("MONGO_URI environment variable is not set. Check backend/.env")

# MongoDB Connection
client = MongoClient(MONGO_URI)
db     = client[MONGO_DB_NAME]
orders = db["orders"]


def serialize_doc(doc):
    """Convert MongoDB ObjectId to string."""
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc


# ───────────────── Create Order ─────────────────
@app.route("/api/orders", methods=["POST"])
def create_order():

    data = request.get_json(silent=True) or {}

    username   = data.get("username")
    cart_items = data.get("items", [])
    total      = data.get("total", 0)

    if not username or not cart_items:
        return jsonify({"error": "Invalid order data"}), 400

    order_id = str(uuid.uuid4())[:8].upper()

    order_data = {
        "order_id": order_id,
        "username": username,
        "items": cart_items,
        "total": total,
        "timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "Pending"
    }

    orders.insert_one(order_data)
    orders_created_total.inc()

    return jsonify({
        "message": "Order created",
        "order_id": order_id
    }), 201


# ───────────────── Get Order ─────────────────
@app.route("/api/orders/<order_id>", methods=["GET"])
def get_order(order_id):

    username = request.args.get("username")

    query = {"order_id": order_id}

    if username:
        query["username"] = username

    order = orders.find_one(query)

    if not order:
        return jsonify({"error": "Order not found"}), 404

    return jsonify(serialize_doc(order)), 200


# ───────────────── Update Order Status ─────────────────
@app.route("/api/orders/<order_id>", methods=["PUT"])
def update_order_status(order_id):

    data = request.get_json(silent=True) or {}
    status = data.get("status")

    if not status:
        return jsonify({"error": "Status is required"}), 400

    result = orders.update_one(
        {"order_id": order_id},
        {"$set": {"status": status}}
    )

    if result.matched_count == 0:
        return jsonify({"error": "Order not found"}), 404

    updated = orders.find_one({"order_id": order_id})

    return jsonify({
        "message": "Order updated successfully",
        "order": serialize_doc(updated)
    }), 200


# ───────────────── Cancel Order ─────────────────
@app.route("/api/orders/<order_id>/cancel", methods=["PUT"])
def cancel_order(order_id):

    data = request.get_json(silent=True) or {}
    username = data.get("username")

    query = {"order_id": order_id}

    if username:
        query["username"] = username

    result = orders.update_one(
        query,
        {"$set": {"status": "Cancelled"}}
    )

    if result.matched_count == 0:
        return jsonify({"error": "Order not found"}), 404

    return jsonify({"message": "Order cancelled"}), 200


# ───────────────── Get User Orders ─────────────────
@app.route("/api/orders/user/<username>", methods=["GET"])
def get_user_orders(username):

    user_orders = [
        serialize_doc(order)
        for order in orders.find({"username": username})
    ]

    return jsonify(user_orders), 200


# ───────────────── Health Check ─────────────────
@app.route("/health", methods=["GET"])
@metrics.do_not_track()
def health():
    return jsonify({"status": "ok", "service": "order_service"}), 200


# ───────────────── Run Server ─────────────────
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)