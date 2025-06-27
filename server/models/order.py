from server.extensions import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_price = db.Column(db.Numeric, nullable=False)
    status = db.Column(db.String(20), default='pending', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', back_populates='orders')
    order_products = db.relationship('OrderProduct', back_populates='order', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Order {self.id} by User {self.user_id}>'


class OrderProduct(db.Model):
    __tablename__ = 'order_products'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price = db.Column(db.Numeric, nullable=False)  

    order = db.relationship('Order', back_populates='order_products')
    product = db.relationship('Product', back_populates='order_items')

    def __repr__(self):
        return f'<OrderProduct order:{self.order_id} product:{self.product_id} quantity:{self.quantity}>'
