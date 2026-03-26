from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Gauge
import os

app = Flask(__name__)
metrics = PrometheusMetrics(app)
metrics.info('product_service_info', 'Product service info', version='1.0')

product_count_gauge = Gauge(
    'product_service_product_count',
    'Total number of products in the catalogue'
)

# ─── Configuration ───────────────────────────────────────────────────────────

MONGO_URI     = os.environ.get("MONGO_URI")
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME", "bakery")

PORT  = int(os.environ.get("PRODUCT_SERVICE_PORT", 5002))
DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"

if not MONGO_URI:
    raise RuntimeError("MONGO_URI environment variable is not set. Check backend/.env")

client   = MongoClient(MONGO_URI)
db       = client[MONGO_DB_NAME]
products = db["products"]

# Create indexes (faster queries)
products.create_index("name")
products.create_index("category")


# ─── Seed Data ───────────────────────────────────────────────────────────────

SEED_PRODUCTS = [
    {"name": "Multigrain Bread",  "price": 80,  "image": "Multigrain_bread.jpg",  "category": "Bread"},
    {"name": "Whole Wheat Bread", "price": 70,  "image": "whole_wheat_bread.jpg", "category": "Bread"},
    {"name": "White Bread",       "price": 60,  "image": "white_bread.jpg",       "category": "Bread"},
    {"name": "Garlic Bread",      "price": 90,  "image": "garlic_bread.jpg",      "category": "Bread"},
    {"name": "Dinner Rolls",      "price": 50,  "image": "dinner_rolls.jpg",      "category": "Bread"},

    {"name": "Blueberry Muffin",  "price": 150, "image": "muffin.jpg",            "category": "Cakes"},
    {"name": "Vanilla Cake",      "price": 400, "image": "vanilla_cake.jpg",      "category": "Cakes"},
    {"name": "Red Velvet Cake",   "price": 550, "image": "red_velvet_cake.jpg",   "category": "Cakes"},
    {"name": "Black Forest Cake", "price": 600, "image": "black_forest_cake.jpg", "category": "Cakes"},
    {"name": "Carrot Cake",       "price": 450, "image": "carrot_cake.jpg",       "category": "Cakes"},
    {"name": "Cheesecake",        "price": 650, "image": "cheesecake.jpg",        "category": "Cakes"},
    {"name": "Fruit Cake",        "price": 500, "image": "fruit_cake.jpg",        "category": "Cakes"},
    {"name": "Chocolate Cake",    "price": 500, "image": "chocolate_cake.jpg",    "category": "Cakes"},

    {"name": "Strawberry Pastry", "price": 180, "image": "pastry.jpg",            "category": "Pastries"},
    {"name": "Donut",             "price": 90,  "image": "donut.jpg",             "category": "Pastries"},
    {"name": "Danish Pastry",     "price": 140, "image": "danish_pastry.jpg",     "category": "Pastries"},
    {"name": "Cinnamon Roll",     "price": 130, "image": "cinnamon_roll.jpg",     "category": "Pastries"},
    {"name": "Croissant",         "price": 120, "image": "croissant.jpg",         "category": "Pastries"},
    {"name": "Apple Strudel",     "price": 150, "image": "apple_strudel.jpg",     "category": "Pastries"},
    {"name": "Puff Pastry",       "price": 110, "image": "puff_pastry.jpg",       "category": "Pastries"},
]


def seed_products():
    """Seed database if empty."""
    if products.count_documents({}) == 0:
        products.insert_many(SEED_PRODUCTS)
        print(f"✅ Seeded {len(SEED_PRODUCTS)} products")
    else:
        print("ℹ️ Products already exist, skipping seed")


seed_products()


# ─── Helpers ─────────────────────────────────────────────────────────────────

def serialize_doc(doc):
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc


# ─── Routes ──────────────────────────────────────────────────────────────────

@app.route("/api/products", methods=["GET"])
def get_products():
    items = [serialize_doc(p) for p in products.find()]
    return jsonify(items), 200


@app.route("/api/products/search", methods=["GET"])
def search_products():

    query = request.args.get("q", "")

    results = [
        serialize_doc(p)
        for p in products.find({
            "name": {"$regex": query, "$options": "i"}
        })
    ]

    return jsonify(results), 200


@app.route("/api/products/category/<cat>", methods=["GET"])
def get_products_by_category(cat):

    items = [
        serialize_doc(p)
        for p in products.find({"category": cat})
    ]

    return jsonify(items), 200


@app.route("/api/products/<product_id>", methods=["GET"])
def get_product(product_id):

    try:
        product = products.find_one({"_id": ObjectId(product_id)})
    except Exception:
        return jsonify({"error": "Invalid product ID"}), 400

    if not product:
        return jsonify({"error": "Product not found"}), 404

    return jsonify(serialize_doc(product)), 200


@app.route("/api/products", methods=["POST"])
def add_product():

    data = request.get_json(silent=True) or {}

    name     = data.get("name")
    price    = data.get("price")
    image    = data.get("image")
    category = data.get("category")

    if not name or price is None:
        return jsonify({"error": "Invalid product data"}), 400

    result = products.insert_one({
        "name": name,
        "price": int(price),
        "image": image,
        "category": category
    })

    return jsonify({
        "message": "Product added",
        "id": str(result.inserted_id)
    }), 201


@app.route("/api/products/<id>", methods=["PUT"])
def update_product(id):

    data = request.get_json(silent=True) or {}
    price = data.get("price")

    if price is None:
        return jsonify({"error": "Price required"}), 400

    products.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"price": int(price)}}
    )

    return jsonify({"message": "Product updated"}), 200


@app.route("/api/products/<id>", methods=["DELETE"])
def delete_product(id):

    products.delete_one({"_id": ObjectId(id)})

    return jsonify({"message": "Product deleted"}), 200


# ─── Health Check ────────────────────────────────────────────────────────────

@app.route("/health", methods=["GET"])
@metrics.do_not_track()
def health():
    count = products.count_documents({})
    product_count_gauge.set(count)
    return jsonify({
        "status": "ok",
        "service": "product_service",
        "product_count": count
    }), 200


# ─── Run Server ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)