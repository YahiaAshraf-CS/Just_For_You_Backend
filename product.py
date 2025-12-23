from flask import app
from flask import request, jsonify,Blueprint
from models import Product
app = Blueprint('product', __name__)
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
@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    result = {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "stock": product.stock,
        "category": product.category,
        "image": product.image
    }
    return jsonify(result), 200