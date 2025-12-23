from flask import Flask, send_from_directory
from flask_cors import CORS
from auth.signup import app as signup_app
from auth.login import app as login_app
from Admin.manageUsers import app as manageUsers_app
from Admin.Dashboard import app as dashboard_app
from add_to_cart import app as addtoCart_app
from product import app as product_app
from wishlist import app as wishlist_app
from orders import app as orders_app
from models import db
app = Flask(__name__)
CORS(app)
print(f"Instance path: {app.instance_path}")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/products'
db.init_app(app)
with app.app_context():
    db.create_all()
app.register_blueprint(signup_app, url_prefix="/api")
app.register_blueprint(login_app, url_prefix="/api")
app.register_blueprint(manageUsers_app, url_prefix="/api/admin")
app.register_blueprint(dashboard_app, url_prefix="/api/admin")
app.register_blueprint(addtoCart_app, url_prefix="/api")
app.register_blueprint(wishlist_app, url_prefix="/api")
app.register_blueprint(orders_app, url_prefix="/api")
app.register_blueprint(product_app, url_prefix="/api")
@app.route('/static/products/<path:filename>')
def serve_product_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
@app.route("/instance")
def instance():
    return app.instance_path

if __name__ == "__main__":
    app.run(debug=True)