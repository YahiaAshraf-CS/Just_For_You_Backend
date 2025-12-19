from flask import Flask
from flask_cors import CORS
from auth.signup import app as signup_app
from Admin.manageUsers import app as manageUsers_app
from add_to_cart import app as addtoCart_app
from orders import app as orders_app
from models import db
app = Flask(__name__)
CORS(app)
print(f"Instance path: {app.instance_path}")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()
app.register_blueprint(signup_app, url_prefix="/api")
app.register_blueprint(manageUsers_app, url_prefix="/api/admin")
app.register_blueprint(addtoCart_app, url_prefix="/api/shop")
app.register_blueprint(orders_app, url_prefix="/api/shop")
@app.route("/instance")
def instance():
    return app.instance_path

if __name__ == "__main__":
    app.run(debug=True)