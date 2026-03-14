import os
from pymongo import MongoClient

mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(mongo_uri)

db = client["bakery"]
products = db["products"]

products.insert_many([

    # 🥖 BREAD
    {"name": "Multigrain Bread", "price": 80, "image": "Multigrain_bread.jpg", "category": "Bread"},
    {"name": "Whole Wheat Bread", "price": 70, "image": "whole_wheat_bread.jpg", "category": "Bread"},
    {"name": "White Bread", "price": 60, "image": "white_bread.jpg", "category": "Bread"},
    {"name": "Garlic Bread", "price": 90, "image": "garlic_bread.jpg", "category": "Bread"},
    {"name": "Dinner Rolls", "price": 50, "image": "dinner_rolls.jpg", "category": "Bread"},

    # 🧁 NEW CAKES
    {"name": "Blueberry Muffin", "price": 150, "image": "muffin.jpg", "category": "Cakes"},
    {"name": "Vanilla Cake", "price": 400, "image": "vanilla_cake.jpg", "category": "Cakes"},
    {"name": "Red Velvet Cake", "price": 550, "image": "red_velvet_cake.jpg", "category": "Cakes"},
    {"name": "Black Forest Cake", "price": 600, "image": "black_forest_cake.jpg", "category": "Cakes"},
    {"name": "Carrot Cake", "price": 450, "image": "carrot_cake.jpg", "category": "Cakes"},
    {"name": "Cheesecake", "price": 650, "image": "cheesecake.jpg", "category": "Cakes"},
    {"name": "Fruit Cake", "price": 500, "image": "fruit_cake.jpg", "category": "Cakes"},
    {"name": "Chocolate Cake", "price": 500, "image": "chocolate_cake.jpg", "category": "Cakes"},
    # 🥐 NEW PASTRIES
    {"name": "Strawberry Pastry", "price": 180, "image": "pastry.jpg", "category": "Pastries"},
    {"name": "Donut", "price": 90, "image": "donut.jpg", "category": "Pastries"},
    {"name": "Danish Pastry", "price": 140, "image": "danish_pastry.jpg", "category": "Pastries"},
    {"name": "Cinnamon Roll", "price": 130, "image": "cinnamon_roll.jpg", "category": "Pastries"},
    {"name": "Croissant", "price": 120, "image": "croissant.jpg", "category": "Pastries"},
    {"name": "Apple Strudel", "price": 150, "image": "apple_strudel.jpg", "category": "Pastries"},
    {"name": "Puff Pastry", "price": 110, "image": "puff_pastry.jpg", "category": "Pastries"},
])

print("New Products Added Successfully!")
