from .user import User
from .product import Product
from .order import Order
from .order_product import OrderProduct
from .transaction import Transaction
from .comment import Comment  

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()