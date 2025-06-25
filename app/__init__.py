from flask import Flask
from .config import Config
from .extensions import db, jwt, ma, limiter,migrate

def create_app():
    app=Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)

    # we'll register the blueprints here

    return app