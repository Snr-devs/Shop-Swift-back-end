from app import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    description = db.Column(db.Text)
    stock = db.Column(db.Integer, nullable=False, default=0)
    image_url = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    category = db.Column(db.String)

   
    order_items = db.relationship('OrderProduct', back_populates='product')

    def __init__(self, name, price, description=None, stock=0, image_url=None, category=None):
        self.name = name
        self.price = price
        self.description = description
        self.stock = stock
        self.image_url = image_url
        self.category = category

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'stock': self.stock,
            'image_url': self.image_url,
            'category': self.category,
            'created_at': self.created_at
            'updated_at': self.updated_at
        }

    def update_stock(self, quantity):
       
        self.stock += quantity
        db.session.commit()

    def __repr__(self):
        return f'<Product {self.name}>'