from extensions import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    description = db.Column(db.Text)
    stock = db.Column(db.Integer, nullable=False, default=0)
    image_url = db.Column(db.String)
    category = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    order_items = db.relationship('OrderProduct', back_populates='product', cascade='all, delete-orphan')

    def __init__(self, name, price, description=None, stock=0, image_url=None, category=None):
        self.name = name
        self.price = price
        self.description = description
        self.stock = stock
        self.image_url = image_url
        self.category = category

    def update_stock(self, quantity):
        self.stock += quantity
        db.session.commit()

    def __repr__(self):
        return f'<Product {self.name}>'
