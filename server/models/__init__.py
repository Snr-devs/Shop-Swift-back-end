from .user import User
from .product import Product
from .order import Order, OrderProduct
from .comment import Comment  
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()