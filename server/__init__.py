from flask import Flask
from .config import Config
from .extensions import db, jwt, ma, limiter, migrate
from server.controllers.product_controller import product_bp
from server.controllers.order_controller import order_bp
from server.controllers.user_controller import user_bp
# from server.controllers.transaction_controller import transaction_bp
from server.controllers.comment_controller import comment_bp
from server.controllers.auth_controller import auth_bp
from flask_cors import CORS



def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)

    @app.route("/")
    def home():
        return {"message": "Welcome to my API"}

   
    app.register_blueprint(product_bp)
    app.register_blueprint(order_bp, url_prefix="/orders")
    app.register_blueprint(user_bp)
    app.register_blueprint(comment_bp)
    app.register_blueprint(auth_bp)
 


    return app 
