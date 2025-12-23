from flask import Blueprint, request, jsonify   
from models import User, Wishlist,db , Cart, Order

app = Blueprint('manageUsers', __name__)
@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    users_list = [{
        "id": user.id,
        "firstName": user.firstName,
        "lastName": user.lastName,
        "number": user.number,
        "email": user.email,
        "is_admin": user.is_admin
    } for user in users]
    return jsonify({"status": "success", "users": users_list}), 200
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404
    cart_items = Cart.query.filter_by(user_id=user_id).all()
    for item in cart_items:
        db.session.delete(item)
    wishlist_items = Wishlist.query.filter_by(user_id=user_id).all()
    for item in wishlist_items:
        db.session.delete(item)
    orders = Order.query.filter_by(user_id=user_id).all()
    for order in orders:
        db.session.delete(order)
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({"status": "success", "message": "User deleted"}), 200
@app.route("/users/<int:user_id>", methods=["POST"])
def promote(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404
    
    user.is_admin = True
    db.session.commit()
    
    return jsonify({"status": "success", "message": "User promoted to admin"}), 200