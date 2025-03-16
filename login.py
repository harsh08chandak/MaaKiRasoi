from flask import Flask, render_template, request, redirect, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = "your_secret_key"

# Simulated database
users = {}
orders = []

@app.route("/")
def home():
    return "Welcome to the E-Commerce Backend!"

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    if username in users and check_password_hash(users[username], password):
        session["user"] = username
        return jsonify({"message": "Login successful!"}), 200
    return jsonify({"message": "Invalid username or password"}), 401

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    if username in users:
        return jsonify({"message": "Username already exists"}), 400
    
    users[username] = generate_password_hash(password)
    return jsonify({"message": "User registered successfully!"}), 201

@app.route("/logout")
def logout():
    session.pop("user", None)
    return jsonify({"message": "Logged out successfully"})

@app.route("/place_order", methods=["POST"])
def place_order():
    if "user" not in session:
        return jsonify({"message": "Unauthorized. Please login first."}), 401
    
    data = request.json
    orders.append({"user": session["user"], "order": data})
    return jsonify({"message": "Order placed successfully!"}), 201

@app.route("/orders", methods=["GET"])
def get_orders():
    if "user" not in session:
        return jsonify({"message": "Unauthorized. Please login first."}), 401
    
    user_orders = [order for order in orders if order["user"] == session["user"]]
    return jsonify(user_orders), 200

if __name__ == "__main__":
    app.run(debug=True)


# python login.html