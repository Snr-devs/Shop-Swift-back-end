import os
from flask.cli import FlaskGroup
from dotenv import load_dotenv

from app.__init__ import create_app
from app.extensions import db
from app.models.user import User
from app.models.product import Product
from app.models.order import Order

load_dotenv()

app = create_app()
cli = FlaskGroup(app)

if __name__ == "__main__":
    cli()
