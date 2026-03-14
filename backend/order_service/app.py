from flask import Flask, request, jsonify
from pymongo import MongoClient
import os
import uuid
import datetime

app = Flask(__name__)

mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/bakery")
client = MongoClient(mongo_uri)
db = client.get_default_database()
orders = db["orders"]

def serialize_doc(doc):
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

# -------------------- Create Order --------------------
@app.route("/api/orders", methods=["POST"])
def create_order():
    data = request.json
    username = data.get("username")
    cart_items = data.get("items", [])
    total = data.get("total", 0)

    if not username or not cart_items:
        return jsonify({"error": "Invalid order data"}), 400

    order_id = str(uuid.uuid4())[:8].upper()

    order_data = {
        "order_id": order_id,
        "username": username,
        "items": cart_items,
        "total": total,
        "timestamp": datetime.datetime.now().strftime("%d-%m-%Y %H:%M"),
        "status": "Pending"
    }

    orders.insert_one(order_data)
    return jsonify({"message": "Order created", "order_id": order_id}), 201

# -------------------- Get Order --------------------
@app.route("/api/orders/<order_id>", methods=["GET"])
def get_order(order_id):
    username = request.args.get("username")
    query = {"order_id": order_id}
    if username:
        query["username"] = username

    order = orders.find_one(query)
    if order:
        return jsonify(serialize_doc(order)), 200
    return jsonify({"error": "Order not found"}), 404

# -------------------- Update Order Status --------------------
@app.route("/api/orders/<order_id>", methods=["PUT"])
def update_order_status(order_id):
    data = request.json
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
    return jsonify({"message": "Order updated successfully", "order": serialize_doc(updated)}), 200

# -------------------- Cancel Order --------------------
@app.route("/api/orders/<order_id>/cancel", methods=["PUT"])
def cancel_order(order_id):
    username = request.json.get("username") if request.json else None
    query = {"order_id": order_id}
    if username:
        query["username"] = username

    result = orders.update_one(query, {"$set": {"status": "Cancelled"}})

    if result.matched_count == 0:
        return jsonify({"error": "Order not found"}), 404

    return jsonify({"message": "Order cancelled"}), 200

# -------------------- Get User Orders --------------------
@app.route("/api/orders/user/<username>", methods=["GET"])
def get_user_orders(username):
    user_orders = [serialize_doc(o) for o in orders.find({"username": username})]
    return jsonify(user_orders), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)
