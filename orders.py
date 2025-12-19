from flask import Blueprint, request, jsonify   
from models import Product, User, Cart, Order, db 
app = Blueprint('orders', __name__)
@app.route("/orders", methods=["POST"])
def place_order():
    data = request.get_json()
    user_id = data.get("user_id")

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    cart_items = Cart.query.filter_by(user_id=user_id).all()
    if not cart_items:
        return jsonify({"message": "Cart is empty"}), 400

    orders = []
    total = 0
    for item in cart_items:
        product = item.product
        if product.stock < item.quantity:
            return jsonify({"message": f"Insufficient stock for {product.name}"}), 400

        product.stock -= item.quantity
        order = Order(user_id=user_id, product_id=item.product_id, quantity=item.quantity, total_price=product.price * item.quantity)
        db.session.add(order)
        orders.append({
            "product_id": item.product_id,
            "quantity": item.quantity,
            "total_price": product.price * item.quantity
        })
        total += product.price * item.quantity

    Cart.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    return jsonify({"message": "Order placed successfully", "orders": orders, "total": total}), 201

@app.route("/orders/<int:user_id>", methods=["GET"])
def get_orders(user_id):
    orders = Order.query.filter_by(user_id=user_id).all()
    result = []
    for o in orders:
        result.append({
            "id": o.id,
            "product_id": o.product_id,
            "product_name": o.product.name,
            "quantity": o.quantity,
            "total_price": o.total_price,
            "order_date": o.order_date
        })
    return jsonify(result), 200