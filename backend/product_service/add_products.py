import os
from pymongo import MongoClient

# ─── Configuration ───────────────────────────────────────────────────────────

MONGO_URI = os.environ.get("MONGO_URI")
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME", "bakery")

if not MONGO_URI:
    raise RuntimeError("MONGO_URI environment variable is not set. Check backend/.env")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]
products = db["products"]

# Create indexes (faster queries)
products.create_index("name")
products.create_index("category")

# ─── Product Data ────────────────────────────────────────────────────────────

SEED_PRODUCTS = [

    # 🥖 BREAD
    {"name": "Multigrain Bread",  "price": 80,  "image": "Multigrain_bread.jpg",  "category": "Bread"},
    {"name": "Whole Wheat Bread", "price": 70,  "image": "whole_wheat_bread.jpg", "category": "Bread"},
    {"name": "White Bread",       "price": 60,  "image": "white_bread.jpg",       "category": "Bread"},
    {"name": "Garlic Bread",      "price": 90,  "image": "garlic_bread.jpg",      "category": "Bread"},
    {"name": "Dinner Rolls",      "price": 50,  "image": "dinner_rolls.jpg",      "category": "Bread"},

    # 🧁 CAKES
    {"name": "Blueberry Muffin",  "price": 150, "image": "muffin.jpg",            "category": "Cakes"},
    {"name": "Vanilla Cake",      "price": 400, "image": "vanilla_cake.jpg",      "category": "Cakes"},
    {"name": "Red Velvet Cake",   "price": 550, "image": "red_velvet_cake.jpg",   "category": "Cakes"},
    {"name": "Black Forest Cake", "price": 600, "image": "black_forest_cake.jpg", "category": "Cakes"},
    {"name": "Carrot Cake",       "price": 450, "image": "carrot_cake.jpg",       "category": "Cakes"},
    {"name": "Cheesecake",        "price": 650, "image": "cheesecake.jpg",        "category": "Cakes"},
    {"name": "Fruit Cake",        "price": 500, "image": "fruit_cake.jpg",        "category": "Cakes"},
    {"name": "Chocolate Cake",    "price": 500, "image": "chocolate_cake.jpg",    "category": "Cakes"},

    # 🥐 PASTRIES
    {"name": "Strawberry Pastry", "price": 180, "image": "pastry.jpg",            "category": "Pastries"},
    {"name": "Donut",             "price": 90,  "image": "donut.jpg",             "category": "Pastries"},
    {"name": "Danish Pastry",     "price": 140, "image": "danish_pastry.jpg",     "category": "Pastries"},
    {"name": "Cinnamon Roll",     "price": 130, "image": "cinnamon_roll.jpg",     "category": "Pastries"},
    {"name": "Croissant",         "price": 120, "image": "croissant.jpg",         "category": "Pastries"},
    {"name": "Apple Strudel",     "price": 150, "image": "apple_strudel.jpg",     "category": "Pastries"},
    {"name": "Puff Pastry",       "price": 110, "image": "puff_pastry.jpg",       "category": "Pastries"},
]

# ─── Insert Data ─────────────────────────────────────────────────────────────

existing_count = products.count_documents({})

if existing_count > 0:
    print(f"ℹ️ Products already exist ({existing_count} found). Skipping seed.")
else:
    result = products.insert_many(SEED_PRODUCTS)
    print(f"✅ Inserted {len(result.inserted_ids)} products successfully!")