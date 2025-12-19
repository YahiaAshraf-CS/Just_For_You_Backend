from flask import Blueprint, request, jsonify
from models import Product, User, Wishlist, db

wishlist_bp = Blueprint("wishlist", __name__)

@wishlist_bp.route("/api/wishlist", methods=["POST"])
def add_to_wishlist():
    data = request.get_json()

    user_id = data.get("user_id")
    product_id = data.get("product_id")

    if not user_id or not product_id:
        return jsonify({"message": "Missing user_id or product_id"}), 400


    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404


    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404


    existing = Wishlist.query.filter_by(
        user_id=user_id,
        product_id=product_id
    ).first()

    if existing:
        return jsonify({"message": "Product already in wishlist"}), 409

    wishlist_item = Wishlist(
        user_id=user_id,
        product_id=product_id
    )

    db.session.add(wishlist_item)
    db.session.commit()

    return jsonify({"message": "Added to wishlist"}), 201



@wishlist_bp.route("/api/wishlist/<int:user_id>", methods=["GET"])
def get_wishlist(user_id):
    wishlist_items = Wishlist.query.filter_by(user_id=user_id).all()

    result = []
    for item in wishlist_items:
        result.append({
            "wishlist_id": item.id,
            "product_id": item.product.id,
            "name": item.product.name,
            "price": item.product.price,
            "image": item.product.image,
            "category": item.product.category
        })

    return jsonify(result), 200



@wishlist_bp.route("/api/wishlist/<int:wishlist_id>", methods=["DELETE"])
def remove_from_wishlist(wishlist_id):
    wishlist_item = Wishlist.query.get_or_404(wishlist_id)

    db.session.delete(wishlist_item)
    db.session.commit()

    return jsonify({"message": "Removed from wishlist"}), 200
