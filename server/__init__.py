from flask import Flask
from config import Config
from extensions import db, jwt, ma, limiter, migrate
from controllers.product_controller import product_bp
from controllers.order_controller import order_bp
from controllers.user_controller import user_bp
from controllers.transaction_controller import transaction_bp
from controllers.comment_controller import comment_bp
from controllers.auth_controller import auth_bp
from controllers.task_controller import task_bp


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)

    @app.route("/")
    def home():
        return {"message": "BookBuddies API is up and running!"}

   
    app.register_blueprint(product_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(transaction_bp)
    app.register_blueprint(comment_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)


    return app 
