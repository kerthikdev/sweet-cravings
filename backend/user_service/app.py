from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
import os
import jwt
import datetime

app = Flask(__name__)

SECRET_KEY = os.environ.get("SECRET_KEY", "supersecretkey")
mongo_uri = os.environ.get("MONGO_URI", "mongodb+srv://admin:admin@mongo.s2gflbj.mongodb.net/bakery?retryWrites=true&w=majority&appName=mongo")
client = MongoClient(mongo_uri)
db = client.get_default_database()
users = db["users"]

bcrypt = Bcrypt(app)

# -------------------- Signup --------------------
@app.route("/api/users/signup", methods=["POST"])
def signup():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing credentials"}), 400

    if users.find_one({"username": username}):
        return jsonify({"error": "Username already exists!"}), 400

    hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")
    users.insert_one({"username": username, "password": hashed_pw})

    return jsonify({"message": "User created successfully"}), 201

# -------------------- Login --------------------
@app.route("/api/users/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = users.find_one({"username": username})

    if user and bcrypt.check_password_hash(user["password"], password):
        token = jwt.encode(
            {
                "username": username,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=8)
            },
            SECRET_KEY,
            algorithm="HS256"
        )
        return jsonify({"message": "Login successful", "username": username, "token": token}), 200
    else:
        return jsonify({"error": "Invalid Credentials"}), 401

# -------------------- Verify Token --------------------
@app.route("/api/users/verify", methods=["POST"])
def verify_token():
    data = request.json
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

# -------------------- Get User --------------------
@app.route("/api/users/<username>", methods=["GET"])
def get_user(username):
    user = users.find_one({"username": username})
    if user:
        return jsonify({"username": user["username"]}), 200
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
