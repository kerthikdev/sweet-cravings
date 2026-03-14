from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)

mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/bakery")
client = MongoClient(mongo_uri)
db = client.get_default_database()
products = db["products"]

# ─── Seed Data ───────────────────────────────────────────────────────────────
SEED_PRODUCTS = [
    # 🥖 Bread
    {"name": "Multigrain Bread",   "price": 80,  "image": "Multigrain_bread.jpg",   "category": "Bread"},
    {"name": "Whole Wheat Bread",  "price": 70,  "image": "whole_wheat_bread.jpg",  "category": "Bread"},
    {"name": "White Bread",        "price": 60,  "image": "white_bread.jpg",        "category": "Bread"},
    {"name": "Garlic Bread",       "price": 90,  "image": "garlic_bread.jpg",       "category": "Bread"},
    {"name": "Dinner Rolls",       "price": 50,  "image": "dinner_rolls.jpg",       "category": "Bread"},
    # 🧁 Cakes
    {"name": "Blueberry Muffin",   "price": 150, "image": "muffin.jpg",             "category": "Cakes"},
    {"name": "Vanilla Cake",       "price": 400, "image": "vanilla_cake.jpg",       "category": "Cakes"},
    {"name": "Red Velvet Cake",    "price": 550, "image": "red_velvet_cake.jpg",    "category": "Cakes"},
    {"name": "Black Forest Cake",  "price": 600, "image": "black_forest_cake.jpg",  "category": "Cakes"},
    {"name": "Carrot Cake",        "price": 450, "image": "carrot_cake.jpg",        "category": "Cakes"},
    {"name": "Cheesecake",         "price": 650, "image": "cheesecake.jpg",         "category": "Cakes"},
    {"name": "Fruit Cake",         "price": 500, "image": "fruit_cake.jpg",         "category": "Cakes"},
    {"name": "Chocolate Cake",     "price": 500, "image": "chocolate_cake.jpg",     "category": "Cakes"},
    # 🥐 Pastries
    {"name": "Strawberry Pastry",  "price": 180, "image": "pastry.jpg",             "category": "Pastries"},
    {"name": "Donut",              "price": 90,  "image": "donut.jpg",              "category": "Pastries"},
    {"name": "Danish Pastry",      "price": 140, "image": "danish_pastry.jpg",      "category": "Pastries"},
    {"name": "Cinnamon Roll",      "price": 130, "image": "cinnamon_roll.jpg",      "category": "Pastries"},
    {"name": "Croissant",          "price": 120, "image": "croissant.jpg",          "category": "Pastries"},
    {"name": "Apple Strudel",      "price": 150, "image": "apple_strudel.jpg",      "category": "Pastries"},
    {"name": "Puff Pastry",        "price": 110, "image": "puff_pastry.jpg",        "category": "Pastries"},
]

def seed_products():
    """Auto-seed products on startup if the collection is empty."""
    if products.count_documents({}) == 0:
        products.insert_many(SEED_PRODUCTS)
        print(f"✅ Seeded {len(SEED_PRODUCTS)} products into database")
    else:
        print(f"ℹ️  Products already exist ({products.count_documents({})} found), skipping seed")

# Run seed on startup
seed_products()

# ─── Helpers ─────────────────────────────────────────────────────────────────
def serialize_doc(doc):
    if doc:
        doc["_id"] = str(doc["_id"])
    return doc

# ─── Routes ──────────────────────────────────────────────────────────────────
@app.route("/api/products", methods=["GET"])
def get_products():
    return jsonify([serialize_doc(p) for p in products.find()]), 200

@app.route("/api/products/search", methods=["GET"])
def search_products():
    query = request.args.get("q", "")
    results = [serialize_doc(p) for p in products.find(
        {"name": {"$regex": query, "$options": "i"}}
    )]
    return jsonify(results), 200

@app.route("/api/products/category/<cat>", methods=["GET"])
def get_products_by_category(cat):
    return jsonify([serialize_doc(p) for p in products.find({"category": cat})]), 200

@app.route("/api/products/<product_id>", methods=["GET"])
def get_product(product_id):
    try:
        product = products.find_one({"_id": ObjectId(product_id)})
        if product:
            return jsonify(serialize_doc(product)), 200
    except Exception:
        pass
    return jsonify({"error": "Product not found"}), 404

@app.route("/api/products", methods=["POST"])
def add_product():
    data = request.json
    result = products.insert_one({
        "name":     data.get("name"),
        "price":    int(data.get("price")),
        "image":    data.get("image"),
        "category": data.get("category")
    })
    return jsonify({"message": "Product added", "id": str(result.inserted_id)}), 201

@app.route("/api/products/<id>", methods=["PUT"])
def update_product(id):
    data = request.json
    products.update_one({"_id": ObjectId(id)}, {"$set": {"price": int(data.get("price"))}})
    return jsonify({"message": "Product updated"}), 200

@app.route("/api/products/<id>", methods=["DELETE"])
def delete_product(id):
    products.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Product deleted"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
