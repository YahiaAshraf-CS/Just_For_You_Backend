from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from models import User

app = Blueprint('login', _name_)

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email", "").lower()
    password = data.get("password")

    if not email or not password:
        return jsonify({"status": "error", "message": "Missing email or password"}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"status": "error", "message": "Invalid email or password"}), 401

    
    if not check_password_hash(user.password, password):
        return jsonify({"status": "error", "message": "Invalid email or password"}), 401

   
    return jsonify({
        "status": "success",
        "message": "Login successful",
        "user": {
            "id": user.id,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "number": user.number,
            "email": user.email
        }
    }), 200