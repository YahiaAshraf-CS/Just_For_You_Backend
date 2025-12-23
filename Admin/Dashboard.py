from flask import Flask, request, jsonify, Blueprint, current_app
from models import Product, db, Cart, Order, Wishlist, User
import os
from werkzeug.utils import secure_filename
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
#edit
UPLOAD_FOLDER = 'static/products'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
@app.route("/products", methods=["POST"])
def add_product():
    try:
        # 1. Get text data using request.form
        name = request.form.get('name')
        price = request.form.get('price')
        description = request.form.get('description')
        stock = request.form.get('stock')
        category = request.form.get('category')

        # 2. Get the file using request.files
        if 'image' not in request.files:
            return jsonify({"status": "error", "message": "No image part"}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({"status": "error", "message": "No selected file"}), 400

        if file:
            # Secure the filename and save it
            filename = secure_filename(file.filename)
            save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)

            # 3. Create the URL to be stored in the database
            # This allows the React frontend to load the image via a URL
            image_url = f"http://127.0.0.1:5000/static/products/{filename}"

            # --- DATABASE LOGIC HERE ---
            new_product = Product(
                name=name,
                description=description,
                price=float(price),
                stock=int(stock),
                category=category,
                image=image_url
            )
            db.session.add(new_product)
            db.session.commit()
            # ---------------------------

            return jsonify({
                "status": "success", 
                "message": "Product added successfully!",
                "image_path": image_url
            }), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

#finish edit
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
    cart_items = Cart.query.filter_by(product_id=product_id).all()
    for item in cart_items:
        db.session.delete(item)
    wishlist_items = Wishlist.query.filter_by(product_id=product_id).all()
    for item in wishlist_items:
        db.session.delete(item)
    orders = Order.query.filter_by(product_id=product_id).all()
    for order in orders:
        db.session.delete(order)
    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": "Product deleted successfully"}), 200


@app.route("/orders", methods=["GET"])
def get_orders():
    orders = Order.query.all()
    result = []
    for o in orders:
        result.append({
            "id": o.id,
            "user_id": o.user_id,
            "user_name":  o.user.firstName + " " + o.user.lastName,
            "product_id": o.product_id,
            "product_name": o.product.name,
            "quantity": o.quantity,
            "total_price": o.total_price,
            "order_date": o.order_date,
            #User.query.get(o.user_id).firstName
        })
    return jsonify(result), 200