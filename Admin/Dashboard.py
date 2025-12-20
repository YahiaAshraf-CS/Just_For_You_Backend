from flask import Flask, request, jsonify,Blueprint
from models import Product, db
app = Blueprint('Dashboard', __name__)
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

@app.route("/products", methods=["POST"])
def add_product():
    data = request.get_json()

    if not all([data.get("name"), data.get("price"), data.get("description"), data.get("stock"), data.get("category"), data.get("image")]):
        return jsonify({"message": "All fields are required"}), 400

    product = Product(
        name=data.get("name"),
        description=data.get("description"),
        price=data.get("price"),
        stock=data.get("stock", 0),
        category=data.get("category"),
        image=data.get("image")
    )

    db.session.add(product)
    db.session.commit()

    return jsonify({"message": "Product added successfully"}), 201

@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.get_json()

    product.name = data.get("name", product.name)
    product.description = data.get("description", product.description)
    product.price = data.get("price", product.price)
    product.stock = data.get("stock", product.stock)
    product.category = data.get("category", product.category)
    product.image = data.get("image", product.image)

    db.session.commit()

    return jsonify({"message": "Product updated successfully"}), 200

@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)

    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": "Product deleted successfully"}), 200