// MongoDB initialization script for the bakery database
// This runs automatically when the mongo container starts for the first time.

db = db.getSiblingDB('bakery');

// Create collections with basic validation
db.createCollection('users');
db.createCollection('products');
db.createCollection('orders');

// Create indexes for performance
db.users.createIndex({ "username": 1 }, { unique: true });
db.orders.createIndex({ "order_id": 1 }, { unique: true });
db.orders.createIndex({ "username": 1 });
db.products.createIndex({ "category": 1 });
db.products.createIndex({ "name": "text" });

print("✅ Bakery database initialized with collections and indexes.");
