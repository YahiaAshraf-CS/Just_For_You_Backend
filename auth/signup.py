from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

app = Blueprint('signup', __name__)

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    firstName = data.get("firstName")
    lastName = data.get("lastName")
    number = data.get("number")
    email = data.get("email").lower()
    password = data.get("password")

    if not all([firstName, lastName, number, email, password]):
        return jsonify({"status": "error", "message": "Missing fields"}), 400
    
    if (len(password) < 6):
        return jsonify({"status": "error", "message": "Password too short"}), 400
    if not any(char.isdigit() for char in password):
        return jsonify({"status": "error", "message": "Password must contain at least one number"}), 400
    if not any(char.isupper() for char in password):
        return jsonify({"status": "error", "message": "Password must contain at least one uppercase character"}), 400   

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"status": "error", "message": "Email already exists"}), 409
    
    hashed_password = generate_password_hash(password)

    new_user = User(
        firstName=firstName,
        lastName=lastName,
        number=number,
        email=email,
        password=hashed_password
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "User registered",
        "user": {
            "id": new_user.id,
            "firstName": new_user.firstName,
            "lastName": new_user.lastName,
            "number": new_user.number,
            "email": new_user.email,
            "is_admin": new_user.is_admin
        }
    }), 201