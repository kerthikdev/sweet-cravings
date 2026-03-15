from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
import os
import jwt
import datetime

app = Flask(__name__)

# ─── Configuration ───────────────────────────────────────────────────────────

MONGO_URI      = os.environ.get("MONGO_URI")
MONGO_DB_NAME  = os.environ.get("MONGO_DB_NAME", "bakery")
SECRET_KEY     = os.environ.get("SECRET_KEY")

PORT  = int(os.environ.get("USER_SERVICE_PORT", 5001))
DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"

JWT_EXPIRY_HOURS = int(os.environ.get("JWT_EXPIRY_HOURS", 8))

if not MONGO_URI:
    raise RuntimeError("MONGO_URI environment variable is not set. Check backend/.env")

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY environment variable is not set. Check backend/.env")

# ─── Database ────────────────────────────────────────────────────────────────

client = MongoClient(MONGO_URI)
db     = client[MONGO_DB_NAME]
users  = db["users"]

# Ensure unique username
users.create_index("username", unique=True)

bcrypt = Bcrypt(app)

# ───────────────── Signup ─────────────────
@app.route("/api/users/signup", methods=["POST"])
def signup():

    data = request.get_json(silent=True) or {}

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing credentials"}), 400

    if users.find_one({"username": username}):
        return jsonify({"error": "Username already exists"}), 400

    hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")

    users.insert_one({
        "username": username,
        "password": hashed_pw
    })

    return jsonify({"message": "User created successfully"}), 201


# ───────────────── Login ─────────────────
@app.route("/api/users/login", methods=["POST"])
def login():

    data = request.get_json(silent=True) or {}

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing credentials"}), 400

    user = users.find_one({"username": username})

    if not user or not bcrypt.check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=JWT_EXPIRY_HOURS)
        },
        SECRET_KEY,
        algorithm="HS256"
    )

    # PyJWT sometimes returns bytes depending on version
    if isinstance(token, bytes):
        token = token.decode("utf-8")

    return jsonify({
        "message": "Login successful",
        "username": username,
        "token": token
    }), 200


# ───────────────── Verify Token ─────────────────
@app.route("/api/users/verify", methods=["POST"])
def verify_token():

    data = request.get_json(silent=True) or {}
    token = data.get("token")

    if not token:
        return jsonify({"error": "Token missing"}), 400

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({"username": payload["username"]}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401

    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401


# ───────────────── Get User ─────────────────
@app.route("/api/users/<username>", methods=["GET"])
def get_user(username):

    user = users.find_one({"username": username})

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"username": user["username"]}), 200


# ───────────────── Run Server ─────────────────
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)