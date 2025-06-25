import os
from flask.cli import FlaskGroup
from dotenv import load_dotenv

from server.__init__ import create_app
from server.extensions import db
from server.models.user import User
from server.models.product import Product
from server.models.order import Order

load_dotenv()

app = create_app()
cli = FlaskGroup(app)

if __name__ == "__main__":
    cli()
