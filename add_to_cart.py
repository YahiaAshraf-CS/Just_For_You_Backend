from flask import Blueprint, request, jsonify   
from models import Product, User, Cart, db 
app = Blueprint('addtoCart_app', __name__)

@app.route("/cart/<int:user_id>", methods=["GET"])
def view_cart(user_id):
    cart_items = Cart.query.filter_by(user_id=user_id).all()
    result = []
    for item in cart_items:
        result.append({
            "id": item.id,
            "product_id": item.product_id,
            "name": item.product.name,
            "description": item.product.description,
            "quantity": item.quantity,
            "price": item.product.price,
            "image": item.product.image,
            "total": item.product.price * item.quantity
        })
    return jsonify(result), 200

@app.route("/cart", methods=["POST"])
def add_to_cart():
    data = request.get_json()
    user_id = data.get("user_id")
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    user = User.query.get(user_id)
    product = Product.query.get(product_id)

    if not user or not product:
        return jsonify({"message": "User or Product not found"}), 404

    existing = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
    total_qty = (existing.quantity if existing else 0) + quantity

    if product.stock < total_qty:
        return jsonify({"message": "Insufficient stock"}), 400

    if existing:
        existing.quantity += quantity
    else:
        cart_item = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)

    db.session.commit()
    return jsonify({"message": "Added to cart"}), 201

@app.route("/cart/<int:cart_id>", methods=["DELETE"])
def remove_from_cart(cart_id):
    cart_item = Cart.query.get(cart_id)
    if not cart_item:
        return jsonify({"message": "Cart item not found"}), 404

    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({"message": "Removed from cart"}), 200

@app.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    result = []
    for p in products:
        result.append({
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "price": p.price,
            "stock": p.stock,
            "category": p.category,
            "image": p.image
        })
    return jsonify(result), 200